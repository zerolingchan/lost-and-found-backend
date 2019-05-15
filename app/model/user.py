from app import db, login_manger
from flask_login import UserMixin as LoginMixin
from sqlalchemy.dialects.mysql import ENUM
from werkzeug.security import check_password_hash, generate_password_hash
from app.util import CommonMixin


class UserModel(LoginMixin, db.Model, CommonMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, comment='主键')
    login = db.Column(db.String(20), comment='账号ID')
    nickname = db.Column(db.String(20), comment='昵称')
    password = db.Column(db.String(128), comment='密码')
    role = db.Column(ENUM('admin', 'user'), nullable=False, comment='用户类型')
    email = db.Column(db.String(20), comment='email')
    comment_ids = db.relationship('CommentModel', backref='user')
    post_ids = db.relationship('PostModel', backref='user')

    def check(self, password):
        """密码验证"""
        return check_password_hash(self.password, password.encode())

    @classmethod
    def validate_login(cls, form):
        """
        验证登陆
        :type form: dict
        :return: UserModel
        :rtype: UserModel
        """
        user = UserModel.exist(login=form['login'], role=form['role'])
        if user is None:
            return None
        elif not user.check(form['password']):
            return None
        return user

    @classmethod
    def register_user(cls, form):
        """
        注册用户
        :type form: dict
        :rtype: UserModel, str
        """
        if form.get('email') and cls.exist(email=form['email']):
            return None, 'email is already exist'
        if cls.exist(login=form['login']):
            return None, 'user is already exist'

        user = cls()
        user.login = form['login']
        user.nickname = form['nickname']
        user.email = form.get('email') or ''
        user.role = 'user'  # 接口只能注册user类型
        password = generate_password_hash(form['password'])
        user.password = password
        db.session.add(user)
        db.session.commit()
        return user, 'register success'

    def asdict(self, columns=None):
        if columns is None:
            columns = ['id', 'login', 'nickname', 'email', 'role']
        return super().asdict(columns)


@login_manger.user_loader
def load_user(uid):
    return db.session.query(UserModel).filter_by(id=uid).first()

