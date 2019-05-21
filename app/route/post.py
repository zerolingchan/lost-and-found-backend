import os
import pathlib
from math import ceil
import logging

from flask import request, Blueprint
from flask_login import login_required, current_user
from flask_restful import Resource
from sqlalchemy.sql import text
from flask_uploads import UploadNotAllowed

from app import uploader, db
from app.forms import PostForm, PaginationForm
from app.model import PostModel
from app.permission import Role
from app.util import hash_filename, json_response


bp_post = Blueprint('post user', __name__)
_logger = logging.getLogger(__name__)


@bp_post.route('/user', methods=['GET'])
@login_required
@json_response
def user_post():
    pagination_form = PaginationForm(meta=dict(csrf=False))
    type = request.values.get('type')
    if not type:
        return dict(code=400, msg='error params', data=None)

    # 由于需要通过子查询当前用户是否点赞，稍微复杂，因此不用orm，手写sql
    key = ('id', 'title', 'content', 'contact', 'type', 'phone', 'image', 'updated_time', 'like')
    sql = text("""
SELECT
    p.id,
    p.title,
    p.content,
    p.contact,
    p.type,
    p.phone,
    p.image,
    p.updated_time,
    IFNULL(( SELECT `status` FROM likes WHERE user_id = :user_id AND post_id = p.id), 0) AS 'like'
FROM
    posts p
WHERE p.type = :type
AND p.deleted = FALSE
AND p.user_id = :user_id
LIMIT :start, :per_page
        """)
    posts = db.engine.execute(sql, type=type,
                              start=pagination_form.per_page.data * (pagination_form.page.data - 1),
                              per_page=pagination_form.per_page.data,
                              user_id=current_user.id if current_user.is_authenticated else 0,).fetchall()

    current_num = len(posts)
    if current_num < pagination_form.per_page.data:
        total_num = len(posts)
    else:
        total_num = PostModel.get_query().filter_by(type=type).count()
    return dict(
        code=200,
        msg='success',
        data=dict(
            data=[dict(zip(key, _)) for _ in posts],
            pagination=dict(
                current_page=pagination_form.page.data,
                current_num=current_num,
                total_page=ceil(total_num / pagination_form.per_page.data),
                total_num=total_num
            )
        )
    )


class Posts(Resource):
    def get(self):
        pagination_form = PaginationForm(meta=dict(csrf=False))
        type = request.values.get('type')
        if not type:
            return dict(code=400, msg='error params', data=None)

        # 由于需要通过子查询当前用户是否点赞，稍微复杂，因此不用orm，手写sql
        key = ('id', 'title', 'content', 'contact', 'type', 'phone', 'image', 'updated_time', 'like')
        sql = text("""
SELECT
    p.id,
    p.title,
    p.content,
    p.contact,
    p.type,
    p.phone,
    p.image,
    p.updated_time,
    IFNULL(( SELECT `status` FROM likes WHERE user_id = :user_id AND post_id = p.id), 0) AS 'like'
FROM
    posts p
WHERE p.type = :type
AND p.deleted = FALSE
LIMIT :start, :per_page
        """)
        posts = db.engine.execute(sql, type=type,
                                  start=pagination_form.per_page.data * (pagination_form.page.data - 1),
                                  per_page=pagination_form.per_page.data,
                                  user_id=current_user.id if current_user.is_authenticated else 0,).fetchall()

        current_num = len(posts)
        if current_num < pagination_form.per_page.data:
            total_num = len(posts)
        else:
            total_num = PostModel.get_query().filter_by(type=type).count()
        return dict(
            code=200,
            msg='success',
            data=dict(
                data=[dict(zip(key, _)) for _ in posts],
                pagination=dict(
                    current_page=pagination_form.page.data,
                    current_num=current_num,
                    total_page=ceil(total_num / pagination_form.per_page.data),
                    total_num=total_num
                )
            )
        )

    @login_required
    def post(self):
        form = PostForm(meta=dict(csrf=False))
        if form.validate():
            path = ''
            try:
                _form = form.form
                del _form['image']  # 文件对象不能直接放数据库，类型不一致
                m = PostModel.new(**_form, user_id=current_user.id, commit=False)

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
                    m.image = 'http://198.13.50.56' + url

                # 提交
                db.session.commit()

                return dict(code=200, msg='success', data=m.asdict())
            except Exception as e:
                _logger.exception(e)
                db.session.rollback()
                # 删除无用附件
                if path:
                    os.remove(pathlib.Path(uploader.config.destination) / path)
                return dict(code=500, msg=str(e), data=None)
        else:
            return form.errors


class Post(Resource):
    def get(self, pid):
        # 由于需要通过子查询当前用户是否点赞，稍微复杂，因此不用orm，手写sql
        sql = text("""
SELECT
    p.id,
    p.title,
    p.content,
    p.contact,
    p.type,
    p.phone,
    p.image,
    p.updated_time,
    IFNULL(( SELECT `status` FROM likes WHERE user_id = :user_id AND post_id = p.id), 0) AS is_like 
FROM
    posts p
WHERE p.id = :pid
AND p.deleted = FALSE
        """)
        post = db.engine.execute(sql, pid=pid, user_id=current_user.id if current_user.is_authenticated else 0).fetchone()

        key = ('id', 'title', 'content', 'contact', 'type', 'phone', 'image', 'updated_time', 'like')
        if post:
            return dict(code=200, msg='success', data=dict(zip(key, post)))
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
