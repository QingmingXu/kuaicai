#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis
import ssl
import json
from datetime import datetime
from urllib import request as url_request
from flask import jsonify, request, Response
from . import api
from .. import db
from ..models import Order, Menu, User

def datetime_to_str(value, format="%Y-%m-%d-%H-%M-%S"):
	return value.strftime(format)

def convert(data):
	if isinstance(data, bytes):
		return data.decode('utf-8')
	if isinstance(data, dict):
		return dict(map(convert, data.items()))
	if isinstance(data, tuple):
		return map(convert, data)
	return data

def list_iter(name):
	redis_pool = redis.ConnectionPool(host='114.116.37.42', port=6379, password='xqm1997', db=0)
	redis_object = redis.StrictRedis(connection_pool=redis_pool)
	list_count = redis_object.llen(name)
	for index in range(list_count):
		yield redis_object.lindex(name, index)

@api.route('/createorder/', methods=['POST'])
def create_order():
	try:
		menu_id = int(json.loads(request.values.get('menu_id')))
		menu_name = str(json.loads(request.values.get('menu_name')))
		user_id = int(json.loads(request.values.get('user_id')))
		num = int(json.loads(request.values.get('num')))
		pay_way = str(json.loads(request.values.get('pay_way')))
		token = str(json.loads(request.values.get('token')))

		menu = Menu.query.filter_by(id=menu_id).first()
		user = User.query.filter_by(id=user_id).first()

		menu.number -= num

		order_content = menu_name + str(num) + '份'
		order_price = num * menu.price
		if (pay_way == 'online'):
			pay_way = '在线支付'
			go_status='未配送'
		else:
			pay_way = '货到付款'
			go_status='配送中'
		order = Order(content=order_content, price=order_price, pay_way=pay_way, pay_status='未支付',
			go_status=go_status, order_status='正常', belong_to=user.id, order_address=user.address)
		db.session.add(order)
		db.session.add(menu)
		db.session.commit()
	except:
		return jsonify({'status': 'error'})
	return jsonify({'status': 'success'})

@api.route('/getuserorders/')
def get_user_orders():
	user_id = request.args.get('user_id')
	orders = Order.query.filter_by(belong_to=int(user_id)).order_by(Order.id.desc()).all()
	return jsonify({'orders': [order.to_json() for order in orders]})

@api.route('/getwaitpayorders/')
def get_wait_pay_orders():
	user_id = request.args.get('user_id')
	status = request.args.get('status')
	orders = Order.query.filter_by(pay_status=status, order_status='正常', belong_to=user_id).order_by(Order.id.desc()).all()
	return jsonify({'orders': [order.to_json() for order in orders]})

@api.route('/getwaitconfrimorders/')
def get_wait_confrim_orders():
	user_id = request.args.get('user_id')
	status = request.args.get('status')
	orders = Order.query.filter_by(order_status='正常', go_status='配送中', belong_to=user_id).order_by(Order.id.desc()).all()
	return jsonify({'orders': [order.to_json() for order in orders]})

@api.route('/getfinishorders/')
def get_finish_orders():
	user_id = request.args.get('user_id')
	status = request.args.get('status')
	orders = Order.query.filter_by(order_status='正常', go_status=status, belong_to=user_id).order_by(Order.id.desc()).all()
	return jsonify({'orders': [order.to_json() for order in orders]})

@api.route('/getcancelorders/')
def get_cancel_orders():
	user_id = request.args.get('user_id')
	status = request.args.get('status')
	orders = Order.query.filter_by(order_status=status, belong_to=user_id).order_by(Order.id.desc()).all()
	return jsonify({'orders': [order.to_json() for order in orders]})

@api.route('/cancelorder/', methods=['POST'])
def cancel_order():
	try:
		order_id = int(json.loads(request.values.get('order_id')))
		order = Order.query.filter_by(id=order_id).first()
		order.order_status = '已取消'
		db.session.add(order)
		db.session.commit()
	except:
		return jsonify({'status': 'error'})
	return jsonify({'status': 'success'})

@api.route('/confrimorder/', methods=['POST'])
def confrim_order():
	try:
		order_id = int(json.loads(request.values.get('order_id')))
		order = Order.query.filter_by(id=order_id).first()
		order.go_status = '配送成功'
		order.pay_status = '已支付'
		db.session.add(order)
		db.session.commit()
	except:
		return jsonify({'status': 'error'})
	return jsonify({'status': 'success'})

'''
@api.route('/putincart/', methods=['POST'])
def put_in_cart():

	user_id = request.values.get('user_id')
	menu_id = request.values.get('menu_id')
	menu_name = request.values.get('menu_name')
	menu_price = request.values.get('menu_price')
	select_num = request.values.get('select_num')
	redis_pool = redis.ConnectionPool(host='114.116.37.42', port=6379, password='xqm1997', db=0)
	redis_object = redis.StrictRedis(connection_pool=redis_pool)
	name_for_redis = 'cart_' + str(user_id)
	key_for_redis = str(menu_id) + '-' + datetime_to_str(datetime.now())
	redis_object.hset(name_for_redis, key_for_redis,
		json.dumps(str(menu_id) + '|' + str(menu_name) + '|' + str(select_num) + '|' + str(menu_price),
		ensure_ascii=False))

	return jsonify({'status': 'success'})
'''

@api.route('/putincart/', methods=['POST'])
def put_in_cart():
	try:
		user_id = int(json.loads(request.values.get('user_id')))
		menu_id = int(json.loads(request.values.get('menu_id')))
		menu_name = str(json.loads(request.values.get('menu_name')))
		menu_price = int(json.loads(request.values.get('menu_price')))
		select_num = int(json.loads(request.values.get('select_num')))
		menu_image_url = str(json.loads(request.values.get('menu_image_url')))

		cart_item = {}
		cart_item['user_id'] = user_id
		cart_item['menu_id'] = menu_id
		cart_item['menu_name'] = menu_name
		cart_item['menu_price'] = menu_price
		cart_item['select_num'] = select_num
		cart_item['menu_image_url'] = menu_image_url
		cart_item['put_in_time'] = datetime_to_str(datetime.now())

		redis_pool = redis.ConnectionPool(host='114.116.37.42', port=6379, password='xqm1997', db=0)
		redis_object = redis.StrictRedis(connection_pool=redis_pool)

		name_for_redis = 'cart_' + str(user_id)
		redis_object.lpush(name_for_redis, json.dumps(cart_item, ensure_ascii=False))
	except Exception as e:
		return jsonify({'status': 'error', 'error_msg': str(e)})
	return jsonify({'status': 'success'})

@api.route('/getshoppingcart/')
def get_cart():
	try:
		user_id = request.values.get('user_id')
		name_for_redis = 'cart_' + str(user_id)
		cart_list = []
		for cart_item in list_iter(name_for_redis):
			cart_list.append(json.loads(cart_item))
	except Exception as e:
		return jsonify({'status': 'error', 'error_msg': str(e)})
	return jsonify({'status': 'success', 'data': cart_list})