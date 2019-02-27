# coding: utf-8
from app import db
import time


class CommonMixin:
    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Boolean, nullable=False, default=False)
    created_time = db.Column(db.Float, default=time.time)
    updated_time = db.Column(db.Float, default=time.time)

    def add_default_value(self):
        pass

    @classmethod
    def exist(cls, **kwargs):
        first = cls.query.filter_by(**kwargs).first()
        return first

    @classmethod
    def new(cls, **kwargs):
        m = cls()
        for name, value in kwargs.items():
            setattr(m, name, value)
        m.add_default_value()
        db.session.add(m)
        db.session.commit()
        return m

    @classmethod
    def delete(cls, id):
        m = cls.update(id=id, deleted=True)
        return m

    @classmethod
    def update(cls, id, **kwargs):
        m = cls.find_by(id=id)
        for name, value in kwargs.items():
            setattr(m, name, value)
        m.updated_time = time.time()
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
