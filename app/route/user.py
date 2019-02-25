from flask import Blueprint, request, jsonify
from ..bean.user import UserForm
from app.model.user import UserModel
from flask_login import login_user, login_required

bp_user = Blueprint('user', __name__)


@bp_user.route('/login', methods=['POST'])
def login():
    form = UserForm(request.form, csrf_enabled=False)
    if form.validate():
        user = UserModel.validate_login(request.form)
        if user:
            login_user(user)
            return 'success'
        else:
            return 'incorrect username or password'
    else:
        return jsonify(form.errors)


@bp_user.route('/register', methods=['POST'])
def register():
    form = UserForm(request.form, csrf_enabled=False)
    if form.validate():
        user, msg = UserModel.register_user(request.form)
        if user:
            return 'ok'
        else:
            return msg
    else:
        return jsonify(form.errors)


@bp_user.route('/test')
@login_required
def test():
    return 'login now'