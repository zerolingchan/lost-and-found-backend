from app import db
from app.util import CommonMixin
from sqlalchemy.dialects.mysql import ENUM


class PostModel(db.Model, CommonMixin):
    """
    失物招领 + 寻物启事 文章
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(ENUM('lost', 'found', 'people'), comment='文章类型')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, comment='用户ID')  # tourists also can post
    contact = db.Column(db.String(20), comment='联系人')
    phone = db.Column(db.String(20), comment='手机号')
    content = db.Column(db.Text, comment='留言内容')
    comment_ids = db.relationship('CommentModel', backref='post')
    attendance_ids = db.relationship('Attendance', backref='post')

    def asdict(self, columns=None):
        if columns is None:
            columns = ['id', 'content', 'type', 'contact', 'phone', 'attendance_ids.path']
        return super().asdict(columns)

