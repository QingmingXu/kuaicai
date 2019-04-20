#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, random, string
from flask import render_template, request, redirect, url_for, current_app, flash
from . import admin
from .forms import AdminForm, EditorAdminForm, ChangePwdForm, NormalChangePwdForm
from ..models import Admin
from ..config import config
from .. import db
from .. import file
from ..pagination import Pagination

# 生成随机的文件名称
def random_name(shuffix, length=16):
	items = string.ascii_letters + string.digits
	return 'kuaicai_' + ''.join([random.choice(items) for i in range(length)]) + '.' + shuffix

@admin.route('/editoradmin', methods=['GET', 'POST'])
def editor_admin():
	editorform = EditorAdminForm()
	if request.method == 'POST':
		if editorform.validate_on_submit():
			admin = Admin.query.filter_by(id=request.args.get('admin_id')).first()
			admin.name = editorform.name.data
			admin.age = editorform.age.data
			admin.phone = editorform.phone.data
			admin.email = editorform.email.data

			if int(request.values.get('is_super')) == 1:
				admin.is_super = True
			else:
				admin.is_super= False

			if int(request.values.get('sex')) == 1:
				admin.sex = '男'
			else:
				admin.sex = '女'

			image = request.files.get('image')
			shuffix = image.filename.split('.')[-1]
			while True:
				image_name = random_name(shuffix)
				path = os.path.join(config['default'].UPLOADED_PHOTOS_DEST, image_name)
				if not os.path.exists(path):
					break
			path_short = '/' + '/'.join(path.split('/')[5:])
			file.save(image, name=image_name)

			admin.image_url_1 = path
			admin.image_url_2 = path_short
			admin.image_name = image_name

			db.session.add(admin)
			db.session.commit()
			flash('修改成功！')
		else:
			flash('修改失败！')
		return redirect(url_for('admin.show_admin') + '?page=' + request.args.get('page'))
	else:
		id_for = request.args.get('admin_id')
		page_num = request.args.get('page_num')
		admin = Admin.query.filter_by(id=id_for).first()
		editorform = EditorAdminForm(name=admin.name, age=admin.age, phone=admin.phone, email=admin.email)
		back_url = url_for('admin.show_admin')
		post_url = url_for('admin.editor_admin')
		return render_template('admin/editor_admin.html', form=editorform, page_num=page_num,
			image_url=admin.image_url_2, back_url=back_url, post_url=post_url, admin_id=id_for,
			admin_sex=admin.sex, admin_level=admin.is_super)

@admin.route('/admin', methods=['GET'])
def show_admin():
	form = AdminForm()
	change_pwd_form = ChangePwdForm()
	normal_change_pwd_form = NormalChangePwdForm()
	admin_list = Admin.query.order_by(Admin.id.desc()).all()
	page_num = request.args.get('page') or 1 
	pagination = Pagination({'page': page_num}, admin_list, 10, 5)
	start = pagination.start
	end = pagination.end
	base_url = url_for('admin.show_admin')
	url_for_editor = url_for('admin.editor_admin')
	return render_template('admin/admin_index.html', form=form, change_pwd_form=change_pwd_form,
		normal_change_pwd_form=normal_change_pwd_form, admin_list=admin_list[start:end],
		page_list=pagination.show_pagination(base_url), page_num=page_num, url_for_editor=url_for_editor)

@admin.route('/addadmin', methods=['POST'])
def add_admin():
	form = AdminForm()
	if form.validate_on_submit():
		if int(request.values.get('sex')) == 1:
			sex = '男'
		else:
			sex = '女'
		if int(request.values.get('is_super')) == 1:
			is_super = True
		else:
			is_super =False
		admin = Admin(name=form.name.data, age=form.age.data, sex=sex, phone=form.phone.data,
			email=form.email.data, is_super=is_super, password=form.password.data)
		db.session.add(admin)
		db.session.commit()
		flash('成功添加了新的管理员，这个新的管理员是' + form.name.data)
	else:
		flash('添加管理员失败！')
	return redirect(url_for('admin.show_admin') + '?page=' + request.args.get('page'))

@admin.route('/deleteadmin', methods=['POST'])
def delete_admin():
	admin = Menu.query.filter_by(id=request.form.get('delete_id')).first()
	db.session.delete(admin)
	db.session.commit()
	flash('删除成功！')
	return redirect(url_for('admin.show_admin') + '?page=' + request.args.get('page_num'))

@admin.route('/superchangepwd', methods=['POST'])
def change_pwd():
	change_pwd_form = ChangePwdForm()
	if change_pwd_form.validate_on_submit():
		password = change_pwd_form.password.data
		admin = Admin.query.filter_by(id=request.args.get('admin_id')).first()
		admin.password = password
		db.session.add(admin)
		db.session.commit()
		flash('成功修改管理员' + admin.name + '的密码！')
	else:
		flash('对管理员' + admin.name + '修改密码失败！')
	return redirect(url_for('admin.show_admin') + '?page=' + request.args.get('page'))

@admin.route('/normalchangepwd', methods=['POST'])
def change_pwd_normal():
	normal_change_pwd_form = NormalChangePwdForm()
	if normal_change_pwd_form.validate_on_submit():
		old_password = normal_change_pwd_form.password_old.data
		admin = Admin.query.filter_by(id=request.args.get('admin_id')).first()
		if admin.verify_password(old_password):
			admin.password = normal_change_pwd_form.password.data
			db.session.add(admin)
			db.session.commit()
			flash('成功修改密码！')
		else:
			flash('旧密码不正确！')
	else:
		flash('修改密码失败！')
	return redirect(url_for('admin.show_admin'))