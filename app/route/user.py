from flask import Blueprint, request
from ..bean.user import UserForm
from app.model.user import UserModel
from flask_login import login_user

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
        return '401'
