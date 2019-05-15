from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FileField
from wtforms.validators import DataRequired, AnyOf, Optional, Email


class BaseForm(FlaskForm):
    @property
    def form(self):
        return dict((name, field.data) for name, field in self._fields.items())


class LoginForm(BaseForm):
    login = StringField('login', validators=[DataRequired('昵称不能为空')])
    password = StringField('password', validators=[DataRequired(message='密码不能为空')])
    role = StringField('login type', validators=[DataRequired('类型不能为空'), AnyOf(['admin', 'user'], message='登陆类型不正确')])


class RegisterForm(BaseForm):
    login = StringField('login', validators=[DataRequired('昵称不能为空')])
    password = StringField('password', validators=[DataRequired(message='密码不能为空')])
    nickname = StringField('nickname', validators=[Optional()])
    email = StringField('email', validators=[Optional(), Email()])


class UserForm(BaseForm):
    """用户修改用户资料"""
    nickname = StringField('nickname', validators=[Optional()])


class PasswordChangeForm(BaseForm):
    old_password = StringField('old_password', validators=[DataRequired('old password is not null')])
    new_password = StringField('new_password', validators=[DataRequired('new password is not null')])


class SearchForm(BaseForm):
    word = StringField('word', validators=[DataRequired()])


class PostForm(BaseForm):
    type = StringField('post type', validators=[DataRequired(), AnyOf(['lost', 'found', 'people'])])
    title = StringField('title', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])
    contact = StringField('contact', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    image = FileField('image', validators=[Optional()])


class PaginationForm(BaseForm):
    page = IntegerField('page num', validators=[Optional()], default=1)
    per_page = IntegerField('per page num', validators=[Optional()], default=20)


class CommentForm(PaginationForm):
    post_id = IntegerField('post id', validators=[DataRequired()])


class NoticeForm(BaseForm):
    title = StringField('title', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])
