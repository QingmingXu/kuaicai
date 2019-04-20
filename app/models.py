#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from flask import url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from . import login_manager

# 装饰器将把load_user注册给flask_login，在需要获取已登录用户时使用
@login_manager.user_loader
def load_user(user_id):
	return Admin.query.get(int(user_id))

class Admin(UserMixin, db.Model):
    __tablename__ = 'tb_admin'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_super = db.Column(db.Boolean)

    sex = db.Column(db.String(16))
    age = db.Column(db.Integer)
    phone = db.Column(db.String(32))

    image_url_1 = db.Column(db.String(128), index=True)
    image_url_2 = db.Column(db.String(128), index=True)
    image_name = db.Column(db.String(128), index=True)

    @property
    def password(self):
        raise AttributeError('password不是一个可读属性！')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Menu(db.Model):
    __tablename__ = 'tb_menu'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    type_name = db.Column(db.String(64))
    info = db.Column(db.String(128), default='暂无资料')
    price = db.Column(db.Float)
    launch_date = db.Column(db.String(64))
    number = db.Column(db.Integer)
    is_grounding = db.Column(db.Boolean, default=True)
    image_url_1 = db.Column(db.String(128), index=True)
    image_url_2 = db.Column(db.String(128), index=True)
    image_name = db.Column(db.String(128), index=True)

    def to_json(self):
        json_menu = {
            'url': url_for('api.get_menus'),
            'menu_id': self.id,
            'menu_name': self.name,
            'menu_type': self.type_name,
            'menu_price': self.price,
            'menu_date': self.launch_date,
            'menu_num': self.number,
            'menu_info': self.info,
            'menu_image_url_1': self.image_url_1,
            'menu_image_url_2': self.image_url_2,
            'menu_image_name': self.image_name
        }
        return json_menu

class User(db.Model):
    __tablename__ = 'tb_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    image_url = db.Column(db.String(1024), index=True)
    user_open_id = db.Column(db.String(1024), index=True)
    address = db.Column(db.String(256))

class Order(db.Model):
    __tablename__ = 'tb_order'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1024))
    price = db.Column(db.Float)
    pay_way = db.Column(db.String(32))
    pay_status = db.Column(db.String(32))
    go_status = db.Column(db.String(32))
    order_status = db.Column(db.String(32))
    belong_to = db.Column(db.Integer, default=0)
    order_time = db.Column(db.DateTime, default=datetime.now)
    order_address = db.Column(db.String(256))

    def to_json(self):
        json_order = {
            'order_id': self.id,
            'order_content': self.content,
            'pay_way': self.pay_way,
            'order_price': self.price,
            'order_time': self.order_time,
            'pay_status': self.pay_status,
            'go_status': self.go_status,
            'order_status': self.order_status,
            'belong_to': self.belong_to,
            'order_address': self.order_address,
        }
        return json_order