from app import db, login_manger
from flask_login import UserMixin as LoginMixin
from sqlalchemy.dialects.mysql import ENUM
from app.common.model import CommonMixin
from werkzeug.security import check_password_hash, generate_password_hash


class UserModel(db.Model, LoginMixin, CommonMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, comment='id')
    login = db.Column(db.String(20), comment='user name')
    nickname = db.Column(db.String(20), comment='user name')
    password = db.Column(db.String(128), comment='password')
    type = db.Column(ENUM('admin', 'user'), comment='user type')
    email = db.Column(db.String(20), comment='email')
    comment_ids = db.relationship('CommentModel', backref='user')

    @classmethod
    def validate_login(cls, form):
        """
        :type form: dict
        :return: UserModel
        :rtype: UserModel
        """
        user = UserModel.exist(login=form['login'], type=form['type'])
        if user is None:
            return None
        elif not check_password_hash(user.password, form['password'].encode()):
            return None
        return user

    @classmethod
    def register_user(cls, form):
        """
        :type form: dict
        :rtype: UserModel, str
        """
        if cls.exist(name=form['login']):
            return None, 'user is already exist'
        if cls.exist(email=form['email']):
            return None, 'email is already exist'

        user = cls()
        user.login = form['login']
        user.nickname = form['nickname']
        user.email = form.get('email') or ''
        user.type = form['type']
        password = generate_password_hash(form['password'])
        user.password = password
        db.session.add(user)
        db.session.commit()
        return user, 'register success'

    def asdict(self):
        return dict(
            login=self.login,
            nickname=self.nickname,
            email=self.email,
            type=self.type
        )


@login_manger.user_loader
def load_user(uid):
    return db.session.query(UserModel).filter_by(id=uid).first()

