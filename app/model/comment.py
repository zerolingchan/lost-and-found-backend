from app import db
from app.common.model import CommonMixin


class CommentModel(db.Model, CommonMixin):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, comment='id')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.String(256))

    def asdict(self, columns=None):
        if columns is None:
            columns = ['id', 'content']
        return super().asdict(columns)
