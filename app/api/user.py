#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis
import ssl
import json
from urllib import request as url_request
from flask import jsonify, request, Response
from . import api
from .. import db
from ..models import User

@api.route('/wxlogin/')
def wxlogin():
	appid = 'wx584b17304af9bd85'
	secret = 'f70e87f0ae1cc45e5c78df94398bf159'
	js_code = request.args.get('code')

	context = ssl._create_unverified_context()
	url = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' %(appid, secret, js_code)
	res = json.loads(url_request.urlopen(url, context=context).read())

	session_key = res['session_key']
	open_id = res['openid']

	if User.query.filter_by(user_open_id=open_id).first() is None:
		name = request.args.get('user_name')
		image_url = request.args.get('user_image_url')
		user = User(name=name, image_url=image_url, user_open_id=open_id)
		db.session.add(user)
		db.session.commit()

	user = User.query.filter_by(user_open_id=open_id).first()

	redis_pool = redis.ConnectionPool(host='114.116.37.42', port=6379, password='xqm1997', db=0)
	redis_object = redis.StrictRedis(connection_pool=redis_pool)
	
	key_for_redis = 'token' + str(user.id)
	if redis_object.exists(key_for_redis):
		redis_object.delete(key_for_redis)
	redis_object.setex(key_for_redis, 604800, json.dumps(open_id + '|' + session_key, ensure_ascii=False))

	return jsonify({'is_show': True, 'token':key_for_redis, 'user_image_url': user.image_url, 'user_id': user.id})

@api.route('/wxloginstate/')
def get_login_state():
	token = request.args.get('token')
	redis_pool = redis.ConnectionPool(host='114.116.37.42', port=6379, password='xqm1997', db=0)
	redis_object = redis.StrictRedis(connection_pool=redis_pool)
	if redis_object.exists(token):
		return jsonify({'loginstate': 'login'})
	else:
		return jsonify({'loginstate': 'nologin'})

@api.route('/wxloginout/')
def wxlogout():
	token = request.args.get('token')
	redis_pool = redis.ConnectionPool(host='114.116.37.42', port=6379, password='xqm1997', db=0)
	redis_object = redis.StrictRedis(connection_pool=redis_pool)
	if redis_object.exists(token):
		redis_object.delete(token)
		return jsonify({'status': 'logout'})
	else:
		return jsonify({'status': 'logout'})

@api.route('/adduseraddress/')
def add_address():
	user_id = request.args.get('user_id')
	address = request.args.get('address')
	try:
		user = User.query.filter_by(id=user_id).first()
		user.address = address
		db.session.add(user)
		db.session.commit()
	except:
		return jsonify({'status': 'error'})
	return jsonify({'status': 'success'})

@api.route('/getaddress/')
def get_address():
	user_id = request.args.get('user_id')
	try:
		user = User.query.filter_by(id=user_id).first()
	except:
		return jsonify({'status': 'error'})
	return jsonify({'status': 'success', 'address': user.address})