#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
	name = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
	password = PasswordField('密码', validators=[DataRequired()])
	submit = SubmitField('登录')
		