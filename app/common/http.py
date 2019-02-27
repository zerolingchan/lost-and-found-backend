from flask import jsonify
from functools import wraps


def json_response(view):
    @wraps(view)
    def wrapped_view(**values):
        result = view(**values)
        if isinstance(result, (dict, list)):
            return jsonify(result)
        else:
            return result
    return wrapped_view