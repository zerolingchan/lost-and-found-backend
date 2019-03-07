from flask import request, Blueprint
from flask_login import login_required, current_user
from app.model.post import PostModel
from app.common.http import json_response
from app.permission import permission_required, Role
from app.forms import PostForm, PaginationForm


bp_post = Blueprint('post', __name__)


# todo 分页器

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
        PostModel.delete(m.id)
        return dict(code=200, msg='success', data=None)
    else:
        return dict(code=404, msg='not found', data=None)
