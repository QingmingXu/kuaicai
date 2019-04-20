#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, FloatField, TextAreaField, RadioField, IntegerField, PasswordField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError
from ..models import Admin
from .. import file

class AdminForm(FlaskForm):
	name = StringField('名字', validators=[DataRequired(), Length(1, 64)])
	age = IntegerField('年龄', validators=[DataRequired()])
	email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
	phone = StringField('电话', validators=[DataRequired(), Length(1, 32)])
	password = PasswordField('密码', validators=[DataRequired(), EqualTo('password_again', message='两次输入的密码需一致！')])
	password_again = PasswordField('确认密码', validators=[DataRequired()])
	submit = SubmitField('确认')

	def validate_email(self, field):
		if Admin.query.filter_by(email=field.data).first():
			raise ValidationError('该邮箱已被注册！')

	def validate_name(self, field):
		if Admin.query.filter_by(name=field.data).first():
			raise ValidationError('该管理员已经存在！')

class EditorAdminForm(FlaskForm):
	name = StringField('名字', validators=[DataRequired(), Length(1, 64)])
	age = IntegerField('年龄', validators=[DataRequired()])
	email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
	phone = StringField('电话', validators=[DataRequired(), Length(1, 32)])
	image = FileField('选择图像', validators=[FileRequired(message='你还没有选择文件！'), FileAllowed(file, message='该文件类型不能上传！')])
	submit = SubmitField('确认编辑')

class ChangePwdForm(FlaskForm):
	password = PasswordField('密码', validators=[DataRequired(), EqualTo('password_again', message='两次输入的密码需一致！')])
	password_again = PasswordField('确认密码', validators=[DataRequired()])
	submit = SubmitField('确认')

class NormalChangePwdForm(FlaskForm):
	password_old = PasswordField('旧密码', validators=[DataRequired()])
	password = PasswordField('密码', validators=[DataRequired(), EqualTo('password_again', message='两次输入的密码需一致！')])
	password_again = PasswordField('确认密码', validators=[DataRequired()])
	submit = SubmitField('确认')