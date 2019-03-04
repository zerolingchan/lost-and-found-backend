from enum import Enum
from flask_login import current_user
from functools import wraps
from flask import abort


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
            if Role[current_user.role] < permission:
                return abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorate_func
