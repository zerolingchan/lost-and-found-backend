from flask import request, Blueprint
from flask_login import login_required, current_user
from app.model.post import PostModel
from app.common.http import json_response
from app import db
from app.permission import permission_required, Role
from app.forms import PostForm


bp_post = Blueprint('post', __name__)


# todo 分页器
# todo 区分不同类型post

@bp_post.route('/<int:id>')
@json_response
def get(id):
    post = PostModel.find_by_id(id)
    if post:
        return dict(code=200, msg='success', data=post.asdict())
    else:
        return dict(code=404, msg='not found', data=None)


@bp_post.route('/all')
@login_required
@permission_required(Role.user)
@json_response
def all():
    posts = PostModel.find_all()
    return dict(
        code=200,
        msg='success',
        data=[_.asdict() for _ in posts]
    )


@bp_post.route('/create', methods=['POST'])
@login_required
@json_response
def create():
    form = PostForm(request.form, meta=dict(csrf=False))
    if form.validate():
        m = PostModel.new(**form.form, user_id=current_user.id)
        return dict(code=200, msg='success', data=m)
    else:
        return form.errors


@bp_post.route('/delete/<int:id>')
@login_required
@json_response
def delete(id):
    m = PostModel.find_one_by(id=id, user_id=current_user.id)
    if m:
        db.session.delete(m)
        db.session.commit()
        return dict(code=200, msg='success', data=None)
    else:
        return dict(code=404, msg='not found', data=None)
