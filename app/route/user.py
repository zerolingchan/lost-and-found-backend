from flask import Blueprint, request, jsonify
from ..bean.user import UserForm
from app.model.user import UserModel
from flask_login import login_user
from app.common import json_response

bp_user = Blueprint('user', __name__)


@bp_user.route('/login', methods=['POST'])
@json_response
def login():
    form = UserForm(request.form, meta=dict(csrf=False))
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
    form = UserForm(request.form, meta=dict(csrf=False))
    if form.validate():
        user, msg = UserModel.register_user(request.form)
        if user:
            return dict(code=200, msg=msg, data=user.asdict())
        else:
            return dict(code=201, msg=msg, data=None)
    else:
        return form.errors
