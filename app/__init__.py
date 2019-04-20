#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, patch_request_class, IMAGES
from .config import config

# SQLAlchemy实例，即用户使用的数据库
db = SQLAlchemy()

# LoginManager实例
login_manager = LoginManager()
# login_view用于设置登录端点。设置后，匿名用户尝试访问受保护页面时，将跳转到登录端点。由于登录路由在蓝图auth中，所以是auth.login
login_manager.login_view = 'auth.login'
file = UploadSet('photos', extensions=('jpg', 'jpeg', 'png'))

def datetimeformat(value, format="%Y-%m-%d/%H:%M"):
	return value.strftime(format)

def create_app(config_name):
	# 创建应用实例
	app = Flask(__name__)
	# 配置
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
    
    # 初始化db，app的配置中有db的相关配置
	db.init_app(app)
    # 初始化login_manager
	login_manager.init_app(app)

	configure_uploads(app, file)
	patch_request_class(app, size=None)

	app.add_template_filter(datetimeformat, 'datetime_format')

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	from .menu import menu as menu_blueprint
	app.register_blueprint(menu_blueprint)

	from .admin import admin as admin_blueprint
	app.register_blueprint(admin_blueprint)

	from .order import order as order_blueprint
	app.register_blueprint(order_blueprint)

	from .api import api as api_blueprint
	app.register_blueprint(api_blueprint, url_prefix='/api/v1')

	return app