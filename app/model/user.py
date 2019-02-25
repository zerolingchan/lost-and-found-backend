from app import db, login_manger
from flask_login import UserMixin as LoginMixin
from sqlalchemy.dialects.mysql import ENUM
from app.common.model import CommonMixin
from werkzeug.security import check_password_hash, generate_password_hash


class UserModel(db.Model, LoginMixin, CommonMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, comment='id')
    name = db.Column(db.String(20), comment='user name')
    password = db.Column(db.String(128), comment='password')
    type = db.Column(ENUM('admin', 'user'), comment='user type')
    email = db.Column(db.String(20), comment='email')

    @classmethod
    def validate_login(cls, form):
        user = UserModel.exist(name=form['name'], type=form['type'])
        if user is None:
            return None
        elif not check_password_hash(user.password, form['password'].encode()):
            return None
        return user

    @classmethod
    def register_user(cls, form):
        if cls.exist(name=form['name']):
            return None, '用户已经存在'
        if cls.exist(email=form['email']):
            return None, '邮件已经被使用'

        user = cls()
        user.name = form['name']
        user.email = form.get('email') or ''
        user.type = form['type']
        password = generate_password_hash(form['password'])
        user.password = password
        db.session.add(user)
        db.session.commit()
        return user, '注册成功'


@login_manger.user_loader
def load_user(uid):
    return db.session.query(UserModel).filter_by(id=uid).first()

