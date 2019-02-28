from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, AnyOf, Optional, Email


class UserForm(FlaskForm):

    login = StringField('login', validators=[DataRequired('昵称不能为空')])
    password = StringField('password', validators=[DataRequired(message='密码不能为空')])
    nickname = StringField('nickname', validators=[Optional()])
    role = StringField('login type', validators=[DataRequired('类型不能为空'), AnyOf(['admin', 'user'], message='登陆类型不正确')])
    email = StringField('email', validators=[Optional(), Email()])
