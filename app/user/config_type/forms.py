# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ConfigTypeForm(FlaskForm):
    name = StringField("配置页名称", validators=[DataRequired("msg_filed_required")])
    submit = SubmitField("提交")
