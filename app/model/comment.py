from app import db
from app.util import CommonMixin


class CommentModel(db.Model, CommonMixin):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, comment='id')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.String(256))

    def asdict(self, columns=None):
        if columns is None:
            columns = ['id', 'title', 'content', 'updated_time']
        return super().asdict(columns)
