from app import db, login_manger
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import ENUM
from app.common.model import CommonMixin
from werkzeug.security import check_password_hash, generate_password_hash


class UserModel(db.Model, UserMixin, CommonMixin):
    id = db.Column(db.Integer, primary_key=True, comment='id')
    name = db.Column(db.String(20), comment='user name')
    password = db.Column(db.String(128), comment='password')
    type = db.Column(ENUM('admin', 'user'), comment='user type')

    @classmethod
    def validate_login(cls, form):
        user = UserModel.exist(name=form['name'])
        if user is None:
            return None
        elif check_password_hash(user.password, form['password']):
            return None
        return user


@login_manger.user_loader
def load_user(uid):
    return db.session.query(UserModel).filter_by(open_id=uid).first()

