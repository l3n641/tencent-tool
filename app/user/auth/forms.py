# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    account = StringField("手机号", validators=[DataRequired("msg_filed_required")])
    password = PasswordField("密码", validators=[DataRequired("msg_filed_required")])
    submit = SubmitField("登陆")