from app import db
from app.util import CommonMixin


class NoticeModel(db.Model, CommonMixin):
    __tablename__ = 'notices'

    id = db.Column(db.Integer, primary_key=True, comment='id')
    title = db.Column(db.String(20), nullable=False, comment='公告标题')
    content = db.Column(db.String(256), nullable=False, comment='公告内容')

    def asdict(self, columns=None):
        if columns is None:
            columns = ['id', 'content', 'title', 'updated_time']
        return super().asdict(columns)
