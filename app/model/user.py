from app import db
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import ENUM


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, comment='id')
    name = db.Column(db.String(20), comment='user name')
    password = db.Column(db.String(128), comment='password')
    type = db.Column(ENUM('admin', 'user'), comment='user type')
