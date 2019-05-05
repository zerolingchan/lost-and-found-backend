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
    title = db.Column(db.String(20), comment='标题')
    phone = db.Column(db.String(20), comment='手机号')
    content = db.Column(db.Text, comment='留言内容')
    comment_ids = db.relationship('CommentModel', backref='post')
    image = db.Column(db.String(256), comment='图片路径')

    def asdict(self, columns=None):
        if columns is None:
            columns = ['id', 'content', 'title', 'updated_time', 'type', 'contact', 'phone', 'image']
        return super().asdict(columns)

