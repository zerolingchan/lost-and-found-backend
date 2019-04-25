from app import db
from app.util import CommonMixin


class NoticeModel(db.Model, CommonMixin):
    __tablename__ = 'notices'

    id = db.Column(db.Integer, primary_key=True, comment='id')
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(256), nullable=False)

    def asdict(self, columns=None):
        if columns is None:
            columns = ['id', 'content', 'title']
        return super().asdict(columns)
