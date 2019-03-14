from flask import jsonify
from functools import wraps
from flask import current_app
from flask_login import current_user
from app import db
import time
import hashlib
from functools import reduce
from os.path import splitext


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


def hash_filename(filename: str):
    filename, ext = splitext(filename)
    return hashlib.md5(filename.encode()).hexdigest() + ext


def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        if isinstance(obj, list):
            return [getattr(o, attr, *args) for o in obj]
        else:
            return getattr(obj, attr, *args)
    return reduce(_getattr, [obj] + attr.split('.'))


class CommonMixin:
    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Boolean, nullable=False, default=False)
    created_time = db.Column(db.Float, default=time.time)
    updated_time = db.Column(db.Float, default=time.time)

    def asdict(self, columns=None):
        """
        输出返回
        :return:
        :rtype: dict
        """
        d = {}
        if columns is None:
            columns = [column.name for column in self.__table__.columns
                       if column.name not in ('deleted', 'created_time', 'updated_time')]
        for column in columns:
            attr = rgetattr(self, column)
            if isinstance(attr, db.Model):
                attr = attr.asdict()
            d[column] = attr
        return d

    def add_default_value(self):
        pass

    @classmethod
    def exist(cls, **kwargs):
        first = cls.query.filter_by(**kwargs).first()
        return first

    @classmethod
    def new(cls, commit=True, **kwargs):
        m = cls()
        for name, value in kwargs.items():
            setattr(m, name, value)
        m.add_default_value()
        if commit:
            db.session.add(m)
            db.session.commit()
        return m

    @classmethod
    def delete(cls, id, commit=True):
        m = cls.update(id, commit, deleted=True)
        return m

    @classmethod
    def update(cls, id, commit=True, **kwargs):
        m = cls.find_by_id(id)
        for name, value in kwargs.items():
            setattr(m, name, value)
        m.updated_time = time.time()
        if commit:
            db.session.add(m)
            db.session.commit()
        return m

    @classmethod
    def find_all(cls, **kwargs):
        ms = cls.query.filter_by(deleted=False, **kwargs).all()
        return ms

    @classmethod
    def find_one_by(cls, **kwargs):
        m = cls.query.filter_by(**kwargs).first()
        return m

    @classmethod
    def find_by_id(cls, id):
        m = cls.query.filter_by(id=id).first()
        return m
