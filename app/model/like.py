from app import db
from app.util import CommonMixin
from sqlalchemy.dialects.mysql import ENUM


class LikeModel(db.Model, CommonMixin):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True, comment='主键')
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False, comment='post表外键')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='user表外键')
    status = db.Column(db.Boolean, comment='点赞状态', nullable=False, default=1)
