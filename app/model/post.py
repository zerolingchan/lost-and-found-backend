from app import db
from app.common.model import CommonMixin
from sqlalchemy.dialects.mysql import ENUM


class PostModel(db.Model, CommonMixin):
    """
    失物招领 + 寻物启事 文章
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(ENUM('lost', 'found'), comment='文章类型')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, comment='留言内容')

    def asdict(self, columns=None):
        if columns is None:
            columns = ['id', 'content', 'type']
        return super().asdict(columns)