from flask import request, Blueprint
from flask_login import login_required, current_user
from flask_uploads import UploadNotAllowed

from app import uploader, db
from app.forms import PostForm, PaginationForm
from app.model import Attendance, PostModel
from app.util import json_response, hash_filename

import os
import pathlib

bp_post = Blueprint('post', __name__)


@bp_post.route('/<int:id>')
@json_response
def get(id):
    post = PostModel.find_by_id(id)
    if post:
        return dict(code=200, msg='success', data=post.asdict())
    else:
        return dict(code=404, msg='not found', data=None)


@bp_post.route('/all')
@json_response
def all():
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


@bp_post.route('/create', methods=['POST'])
@login_required
@json_response
def create():
    form = PostForm(request.form, meta=dict(csrf=False))
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


@bp_post.route('/delete/<int:id>')
@login_required
@json_response
def delete(id):
    m = PostModel.find_one_by(id=id, user_id=current_user.id)
    if m:
        PostModel.delete(m.id)
        return dict(code=200, msg='success', data=None)
    else:
        return dict(code=404, msg='not found', data=None)
