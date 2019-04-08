from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, AnyOf, Optional, Email


class BaseForm(FlaskForm):
    @property
    def form(self):
        return dict((name, field.data) for name, field in self._fields.items())


class UserForm(BaseForm):
    login = StringField('login', validators=[DataRequired('昵称不能为空')])
    password = StringField('password', validators=[DataRequired(message='密码不能为空')])
    nickname = StringField('nickname', validators=[Optional()])
    role = StringField('login type', validators=[DataRequired('类型不能为空'), AnyOf(['admin', 'user'], message='登陆类型不正确')])
    email = StringField('email', validators=[Optional(), Email()])


class PostForm(BaseForm):
    content = StringField('content', validators=[DataRequired()])
    type = StringField('post type', validators=[DataRequired(), AnyOf(['lost', 'found'])])


class PaginationForm(BaseForm):
    page = IntegerField('page num', validators=[Optional()], default=1)
    per_page = IntegerField('per page num', validators=[Optional()], default=20)


class NoticeForm(BaseForm):
    title = StringField('title', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])
