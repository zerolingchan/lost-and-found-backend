from flask import jsonify
from flask_sqlalchemy import BaseQuery
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
    created_time = db.Column(db.Integer, default=lambda: int(time.time()))
    updated_time = db.Column(db.Integer, default=lambda: int(time.time()))

    @classmethod
    def get_query(cls) -> BaseQuery:
        """返回过滤已删除项的查询对象"""
        return cls.query.filter_by(deleted=False)

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
            d[column.split('.')[-1]] = rgetattr(self, column)
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
        m = cls.find_by_id(id)
        m = m.update(commit, deleted=True)
        return m

    def update(self, commit=True, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
        self.updated_time = time.time()
        if commit:
            db.session.add(self)
            db.session.commit()
        return self

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
