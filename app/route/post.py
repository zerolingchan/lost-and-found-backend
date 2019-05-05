import os
import pathlib

from flask import request
from flask_login import login_required, current_user
from flask_restful import Resource
from flask_uploads import UploadNotAllowed

from app import uploader, db
from app.forms import PostForm, PaginationForm
from app.model import PostModel
from app.permission import Role
from app.util import hash_filename


class Posts(Resource):
    def get(self):
        query = PostModel.query.filter_by(deleted=False)
        type = request.values.get('type')
        if type:
            query = query.filter_by(type=type)

        pagination_form = PaginationForm(meta=dict(csrf=False))
        pagination = query.paginate(**pagination_form.form)

        posts = pagination.items
        return dict(
            code=200,
            msg='success',
            data=dict(
                data=[_.asdict() for _ in posts],
                pagination=dict(
                    current_page=pagination.page,
                    current_num=len(posts),
                    total_page=pagination.pages,
                    total_num=pagination.total
                )
            )
        )

    @login_required
    def post(self):
        form = PostForm(meta=dict(csrf=False))
        if form.validate():
            path = ''
            try:
                m = PostModel.new(**form.form, user_id=current_user.id, commit=False)

                # 先flush到数据库，获得ID，下面好根据ID存储文件，但是不提交事务，方便回退
                db.session.add(m)
                db.session.flush()

                image = request.files.get('image')
                if image:
                    filename = hash_filename(image.filename)
                    if not uploader.file_allowed(image, filename):
                        raise UploadNotAllowed('file type not allow')
                    path = uploader.save(storage=image, folder=str(m.id), name=filename)
                    # 获得对应到文件夹路径
                    url = uploader.url(path)
                    m.image = url

                # 提交
                db.session.commit()

                return dict(code=200, msg='success', data=m.asdict())
            except Exception as e:
                db.session.rollback()
                # 删除无用附件
                if path:
                    os.remove(pathlib.Path(uploader.config.destination) / path)
                return dict(code=500, msg=str(e), data=None)
        else:
            return form.errors


class Post(Resource):
    def get(self, pid):
        post = PostModel.find_by_id(pid)
        if post:
            return dict(code=200, msg='success', data=post.asdict())
        else:
            return dict(code=404, msg='not found', data=None)

    @login_required
    def delete(self, pid):
        m = PostModel.find_one_by(id=pid)

        # 如果既不是文章所有者，也不是管理员
        if m.user_id != current_user.id and Role[current_user.role] != Role.admin:
            return dict(code=403, msg='Forbidden', data=None)
        if m:
            PostModel.delete(m.id)
            return dict(code=200, msg='success', data=None)
        else:
            return dict(code=404, msg='not found', data=None)

    @login_required
    def put(self, pid):
        comment = PostModel.find_one_by(id=pid, user_id=current_user.id)
        form = PostForm(meta=dict(csrf=False))
        if comment:
            if form.validate():
                _form = form.form
                # 图片字段不存在时候，NoneType类型无法更新，所以先删除
                del _form['image']

                image = form.image.data
                if image:
                    filename = hash_filename(image.filename)
                    if not uploader.file_allowed(image, filename):
                        raise UploadNotAllowed('file type not allow')
                    path = uploader.save(storage=image, folder=str(comment.id), name=filename)
                    print('path ->', path)
                    # 获得对应到文件夹路径
                    url = uploader.url(path)
                    _form['image'] = url

                comment.update(commit=False, **_form)
                db.session.add(comment)
                db.session.commit()
                return dict(code=200, msg='success', data=comment.asdict())
            else:
                return dict(code=400, msg='form validate failure', data=None)
        else:
            return dict(code=404, msg='not found', data=None)
