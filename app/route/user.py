from flask import Blueprint, request, jsonify, make_response
from flask_login import login_user, login_required, current_user
from werkzeug.security import generate_password_hash

from app import login_manger
from app.forms import LoginForm, RegisterForm, PaginationForm, PasswordChangeForm, UserForm
from app.model.user import UserModel
from app.permission import permission_required, Role
from app.util import json_response
from flask_restful import Resource

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




@bp_user.route('/password/reset', methods=['POST'])
def password_reset():
    """重置密码"""


@bp_user.route('/password/change', methods=['POST'])
@login_required
@json_response
def password_change():
    """修改密码"""
    form = PasswordChangeForm(meta=dict(csrf=False))
    if form.validate():
        if current_user.check(form.old_password.data):
            current_user.update(password=generate_password_hash(form.new_password.data))
            return dict(code=200, msg='success', data=None)
        else:
            return dict(code=40101, msg='密码错误', data=None)
    else:
        return dict(code=400, msg='bad request', data=form.errors)


@login_manger.unauthorized_handler
def unauthorized():
    response = make_response(jsonify(code=40100, msg='unauthorized', data=None), 401)
    return response


class User(Resource):
    @permission_required(Role.admin)
    @json_response
    def delete(self, uid):
        """
        删除用户
        :return:
        """
        users = UserModel.find_by_id(uid)
        if not users:
            return dict(code=404, msg='not found', data=None)
        else:
            UserModel.delete(uid)
            return dict(code=200, msg='success', data=None)

    @login_required
    def put(self, uid):
        """更新用户资料"""
        assert current_user.id == uid  # 断言判断当前用户是本人，十分懒人的处理了，哈哈

        form = UserForm()
        user = UserModel.find_by_id(uid)
        user.update(**form.form)
        return dict(code=200, msg='success', data=user.asdict())
