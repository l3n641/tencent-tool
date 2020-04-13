# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired


class ConfigForm(FlaskForm):
    argument_key = StringField("参数key", validators=[DataRequired("msg_filed_required")])
    argument_description = StringField("参数说明", validators=[DataRequired("msg_filed_required")])
    type = StringField("类型", validators=[DataRequired("msg_filed_required")])
    pre_argument = StringField("预置参数")
    config_type_id = HiddenField("配置类型", validators=[DataRequired("必须")], default=11)
    submit = SubmitField("提交")
