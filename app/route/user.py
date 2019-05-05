from flask import Blueprint, request, jsonify, make_response
from flask_login import login_user

from app import login_manger
from app.forms import LoginForm, RegisterForm, PaginationForm
from app.model.user import UserModel
from app.permission import permission_required, Role
from app.util import json_response

bp_user = Blueprint('user', __name__)


@bp_user.route('/login', methods=['POST'])
@json_response
def login():
    form = LoginForm(meta=dict(csrf=False))
    if form.validate():
        user = UserModel.validate_login(request.form)

        if user:
            login_user(user)
            return dict(code=200, msg='success', data=user.asdict())
        else:
            return dict(code=401, msg='incorrect username or password', data=None)
    else:
        return form.errors


@bp_user.route('/register', methods=['POST'])
@json_response
def register():
    form = RegisterForm(meta=dict(csrf=False))
    if form.validate():
        user, msg = UserModel.register_user(form.form)
        if user:
            return dict(code=200, msg=msg, data=user.asdict())
        else:
            return dict(code=201, msg=msg, data=None)
    else:
        return form.errors


@bp_user.route('/', methods=['GET'])
@permission_required(Role.admin)
@json_response
def get_user():
    """
    分页获得所有用户
    :return:
    """
    pagniate_form = PaginationForm(meta=dict(csrf=False))
    users = UserModel.query.filter_by(deleted=False)\
        .paginate(**pagniate_form.form)
    return dict(
        code=200,
        msg='success',
        data=dict(
            data=[_.asdict() for _ in users.items],
            pagination=dict(
                current_page=users.page,
                current_num=len(users.items),
                total_page=users.pages,
                total_num=users.total
            )
        )
    )


@bp_user.route('/<int:id>', methods=['DELETE'])
@permission_required(Role.admin)
@json_response
def delete_user(id):
    """
    删除用户
    :return:
    """
    users = UserModel.find_by_id(id)
    if not users:
        return dict(code=404, msg='not found', data=None)
    else:
        UserModel.delete(id)
        return dict(code=200, msg='success', data=None)


@login_manger.unauthorized_handler
def unauthorized():
    response = make_response(jsonify(code=40100, msg='unauthorized', data=None), 401)
    return response
