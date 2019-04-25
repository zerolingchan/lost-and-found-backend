from app import db
from app.util import CommonMixin


class LikeModel(db.Model, CommonMixin):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True, comment='id')
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
