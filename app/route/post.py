import os
import pathlib

from werkzeug.datastructures import ImmutableMultiDict
from flask import request
from flask_login import login_required, current_user
from flask_restful import Resource
from flask_uploads import UploadNotAllowed

from app import uploader, db
from app.forms import PostForm, PaginationForm
from app.model import Attendance, PostModel
from app.util import hash_filename


class Posts(Resource):
    def get(self):
        query = PostModel.query.filter_by(deleted=False)
        type = request.values.get('type')
        if type:
            query = query.filter_by(type=type)

        pagination_form = PaginationForm(request.values)
        pagination = query.paginate(**pagination_form.form)

        posts = pagination.items
        return dict(
            code=200,
            msg='success',
            data=dict(
                posts=[_.asdict() for _ in posts],
                current_page=pagination.page,
                current_num=len(posts),
                total_page=pagination.pages,
                total_num=pagination.total
            )
        )

    @login_required
    def post(self):
        form = PostForm(ImmutableMultiDict(request.json), meta=dict(csrf=False))
        if form.validate():
            attendances = []
            try:
                m = PostModel.new(**form.form, user_id=current_user.id, commit=False)
                db.session.add(m)
                db.session.flush()

                # save attendance
                for _, file in request.files.items():
                    filename = hash_filename(file.filename)
                    if not uploader.file_allowed(file, filename):
                        raise UploadNotAllowed('file type not allow')
                    path = uploader.save(storage=file, folder=str(m.id), name=filename)
                    attendances.append(path)
                    url = uploader.url(path)
                    attendance = Attendance.new(commit=False, pid=m.id, path=url)
                    db.session.add(attendance)

                db.session.commit()

                return dict(code=200, msg='success', data=m.asdict())
            except Exception as e:
                db.session.rollback()
                # 删除无用附件
                for path in attendances:
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
        m = PostModel.find_one_by(id=pid, user_id=current_user.id)
        if m:
            PostModel.delete(m.id)
            return dict(code=200, msg='success', data=None)
        else:
            return dict(code=404, msg='not found', data=None)

    # todo 附件更新等内容
    # def put(self, pid):
    #     comment = CommentModel.find_one_by(id=cid, user_id=current_user.id)
    #     if comment:
    #         content = request.form['content']
    #         m = comment.update(content=content)
    #         return dict(code=200, msg='success', data=comment.asdict())
    #     else:
    #         return dict(code=404, msg='not found', data=None)

