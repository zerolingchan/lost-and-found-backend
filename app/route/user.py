from flask import Blueprint, request, jsonify, make_response
from app.forms import LoginForm, RegisterForm
from app.model.user import UserModel
from flask_login import login_user
from app.util import json_response
from app import login_manger

bp_user = Blueprint('user', __name__)


@bp_user.route('/login', methods=['POST'])
@json_response
def login():
    form = LoginForm(request.form, meta=dict(csrf=False))
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
    form = RegisterForm(request.form, meta=dict(csrf=False))
    if form.validate():
        user, msg = UserModel.register_user(form.form)
        if user:
            return dict(code=200, msg=msg, data=user.asdict())
        else:
            return dict(code=201, msg=msg, data=None)
    else:
        return form.errors


@login_manger.unauthorized_handler
def unauthorized():
    response = make_response(jsonify(code=40100, msg='unauthorized', data=None), 401)
    return response
