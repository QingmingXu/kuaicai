#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, random, string
from flask import render_template, request, redirect, url_for, current_app, flash
from . import menu
from .forms import MenuForm, MenuUpdateForm
from ..models import Menu
from ..config import config
from .. import file
from .. import db
from ..pagination import Pagination

# 生成随机的文件名称
def random_name(shuffix, length=16):
	items = string.ascii_letters + string.digits
	return 'kuaicai_' + ''.join([random.choice(items) for i in range(length)]) + '.' +shuffix

# 修改菜品的视图函数
@menu.route('/updatemenu', methods=['GET', 'POST'])
def update_menu():
	form_for_update = MenuUpdateForm()
	if request.method == 'POST':
		if form_for_update.validate_on_submit():
			menu = Menu.query.filter_by(id=request.args.get('menu_id')).first()
			menu.name = form_for_update.name.data
			menu.type_name = form_for_update.type_name.data
			menu.info = form_for_update.info.data
			menu.price = form_for_update.price.data
			menu.launch_date = form_for_update.launchdate.data
			menu.number = form_for_update.number.data

			if int(request.values.get('is_grounding')) == 1:
				menu.is_grounding = True
			else:
				menu.is_grounding = False

			image = request.files.get('image')
			shuffix = image.filename.split('.')[-1]
			while True:
				image_name = random_name(shuffix)
				path = os.path.join(config['default'].UPLOADED_PHOTOS_DEST, image_name)
				if not os.path.exists(path):
					break
			path_short = '/' + '/'.join(path.split('/')[5:])
			file.save(image, name=image_name)

			menu.image_url_1 = path
			menu.image_url_2 = path_short
			menu.image_name = image_name

			db.session.add(menu)
			db.session.commit()
			flash('修改成功！')
		else:
			flash('修改失败！')
		return redirect(url_for('menu.show_menu') + '?page=' + request.args.get('page'))
	else:
		id_for = request.args.get('menu_id')
		page_num = request.args.get('page_num')
		menu = Menu.query.filter_by(id=id_for).first()
		form_for_update = MenuUpdateForm(name=menu.name, type_name=menu.type_name, info=menu.info, price=menu.price,
			launchdate=menu.launch_date, number=menu.number, is_grounding=menu.is_grounding)
		back_url = url_for('menu.show_menu')
		post_url = url_for('menu.update_menu')
		return render_template('menu/show_update_menu.html', form=form_for_update, page_num=page_num,
			image_url=menu.image_url_2, back_url=back_url, post_url=post_url, menu_id=id_for)

# 显示菜品列表的视图函数
@menu.route('/menu', methods=['GET'])
def show_menu():
	# 用于渲染模态框表单的表单类实例
	form = MenuForm()
	# 所有的菜品
	menu_list = Menu.query.order_by(Menu.id.desc()).all()
	page_num = request.args.get('page') or 1 
	pagination = Pagination({'page': page_num}, menu_list, 10, 5)
	start = pagination.start
	end = pagination.end
	base_url = url_for('menu.show_menu')
	url_for_update = url_for('menu.update_menu')
	return render_template('menu/menu_index.html', form=form, menu_list=menu_list[start:end],
		page_list=pagination.show_pagination(base_url), page_num=page_num, url_for_update=url_for_update)

# 添加菜品的视图函数
@menu.route('/addmenu', methods=['GET', 'POST'])
def add_menu():
	form = MenuForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			image = request.files.get('image')
			shuffix = image.filename.split('.')[-1]
			while True:
				image_name = random_name(shuffix)
				path = os.path.join(config['default'].UPLOADED_PHOTOS_DEST, image_name)
				if not os.path.exists(path):
					break
			file.save(image, name=image_name)
			path_short = '/' + '/'.join(path.split('/')[5:])
			menu = Menu(name=form.name.data, type_name=form.type_name.data, info=form.info.data,
				price=form.price.data, launch_date=form.launchdate.data, number=form.number.data,
				is_grounding=True, image_url_1=path, image_url_2=path_short, image_name=image_name)
			db.session.add(menu)
			db.session.commit()
			flash('成功添加菜品，' + '菜品名：' + form.name.data)
		else:
			flash('添加菜品失败！')
		return redirect(url_for('menu.show_menu') + '?page=1')
	else:
		return redirect(url_for('menu.show_menu'))

# 删除菜品的视图函数
@menu.route('/deletemenu', methods=['POST'])
def delete_menu():
	from_page = request.args.get('page_num')
	menu_id = request.form.get('delete_id')
	menu = Menu.query.filter_by(id=menu_id).first()
	db.session.delete(menu)
	db.session.commit()
	flash('删除成功！')
	return redirect(url_for('menu.show_menu') + '?page=' + from_page)		