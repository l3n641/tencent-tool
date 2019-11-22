# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    account = StringField("账号", validators=[DataRequired("msg_filed_required")])
    password = PasswordField("密码", validators=[DataRequired("msg_filed_required")])
    submit = SubmitField("登录")
