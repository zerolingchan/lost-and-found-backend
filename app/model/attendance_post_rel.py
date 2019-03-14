from app import db
from app.util import CommonMixin


class Attendance(db.Model, CommonMixin):
    __tablename__ = 'attendance_post_rel'

    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    path = db.Column(db.String(128))
