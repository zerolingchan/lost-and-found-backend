from app import db
from app.common.model import CommonMixin


class CommentModel(CommonMixin, db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, comment='id')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.String(256))

    def asdict(self):
        return dict(
            id=self.id,
            content=self.content
        )