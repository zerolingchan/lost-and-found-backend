from app import db
from app.util import CommonMixin


class CommentModel(db.Model, CommonMixin):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, nullable=False, comment='主键')
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False, comment='post表外键ID')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='user表外键ID')
    content = db.Column(db.String(256), comment='留言内容')

    def asdict(self, columns=None):
        if columns is None:
            columns = ['id', 'content', 'updated_time']
        return super().asdict(columns)
