from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):

    name = StringField('name', validators=[DataRequired('昵称不能为空')])
    passwd = StringField('password', validators=[DataRequired()])
