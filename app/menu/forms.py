#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, FloatField, TextAreaField, RadioField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length
from .. import file

class MenuForm(FlaskForm):
	name = StringField('名称', validators=[DataRequired(), Length(1, 64)])
	type_name = StringField('类型', validators=[DataRequired(), Length(2,64)])
	info = StringField('描述')
	price = FloatField('价格', validators=[DataRequired()])
	launchdate = StringField('推出日期', validators=[DataRequired()])
	number = FloatField('数量', validators=[DataRequired()])
	image = FileField('选择图片', validators=[FileRequired(message='你还没有选择文件！'), FileAllowed(file, message='该文件类型不能上传！')])
	submit_1 = SubmitField('提交')

class MenuUpdateForm(FlaskForm):
	name = StringField('名称', validators=[DataRequired(), Length(1, 64)])
	type_name = StringField('类型', validators=[DataRequired(), Length(2,64)])
	info = TextAreaField('描述')
	price = FloatField('价格', validators=[DataRequired()])
	launchdate = StringField('推出日期', validators=[DataRequired()])
	number = FloatField('数量', validators=[DataRequired()])
	image = FileField('更换图片', validators=[FileRequired(message='你还没有选择文件！'), FileAllowed(file, message='该文件类型不能上传！')])
	submit = SubmitField('提交修改')