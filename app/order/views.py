#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, random, string
from flask import render_template, request, redirect, url_for, current_app, flash
from . import order
from ..models import Order
from ..config import config
from .. import db
from ..pagination import Pagination

@order.route('/editororder', methods=['POST'])
def editor_order():
	pay_status = request.values.get('pay_status')
	go_status = request.values.get('go_status')
	order_status = request.values.get('order_status')
	order_id = request.values.get('editor_id')

	order = Order.query.filter_by(id=order_id).first()

	if int(pay_status) == 0:
		order.pay_status = '未支付'
	else:
		order.pay_status = '已支付'

	if int(order_status) == 0:
		order.order_status = '已取消'
	else:
		order.order_status = '正常'

	if int(go_status) == 0:
		order.go_status = '未配送'
	elif int(go_status) == 1:
		order.go_status = '配送中'
	else:
		order.go_status = '配送成功'

	db.session.add(order)
	db.session.commit()
	flash('修改订单状态成功')
	return redirect(url_for('order.show_order') + '?page=' + request.args.get('page'))
		
@order.route('/order', methods=['GET'])
def show_order():
	order_list = Order.query.order_by(Order.id.desc()).all()
	page_num = request.args.get('page') or 1 
	pagination = Pagination({'page': page_num}, order_list, 10, 5)
	start = pagination.start
	end = pagination.end
	base_url = url_for('order.show_order')
	return render_template('order/order_index.html', order_list=order_list[start:end],
		page_list=pagination.show_pagination(base_url), page_num=page_num)

@order.route('/deleteorder', methods=['POST'])
def delete_order():
	from_page = request.args.get('page')
	order_id = request.form.get('delete_id')
	order = Order.query.filter_by(id=order_id).first()
	db.session.delete(order)
	db.session.commit()
	flash('删除成功！')
	return redirect(url_for('order.show_order') + '?page=' + from_page)