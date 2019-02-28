from flask import jsonify
from functools import wraps
from flask import request, current_app
from flask_login import current_user


def json_response(view):
    @wraps(view)
    def wrapped_view(**values):
        result = view(**values)
        if isinstance(result, (dict, list)):
            return jsonify(result)
        else:
            return result
    return wrapped_view


def login_required(role='user'):
    """
    override flask_login's login_required function to add the role authentication
    :param role: [user|admin]
    :return:
    """
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_app.login_manager._login_disabled:
                return func(*args, **kwargs)
            elif not current_user.is_authenticated or current_user.role != role:
                return current_app.login_manager.unauthorized()
            return func(*args, **kwargs)
        return decorated_view
    return wrapper
