from enum import Enum
from flask_login import current_user, login_required
from functools import wraps
from flask import jsonify


class Role(Enum):
    """
    用户权限验证，用户权限字段对应model.user中role字段
    """
    user = 1
    admin = 2


def permission_required(permission=Role.user):
    def decorate_func(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # 如果权限级别不够
            print(current_user.is_authenticated, current_user)
            if current_user.is_authenticated and Role[current_user.role].value >= permission.value:
                return f(*args, **kwargs)
            return jsonify(dict(code=401, msg='unauthorized', data=None))
        return wrapper
    return decorate_func
