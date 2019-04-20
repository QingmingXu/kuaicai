#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

class Config:
	SECRET_KEY = '555beiqinle'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAX_CONTENT_LENGTH = 1024*1024*64
	UPLOADED_PHOTOS_DEST = os.path.join(os.getcwd(), 'app/static/uploads')

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:xqm1997@114.116.37.42:5432/kuaicai'

config = {
	'development': DevelopmentConfig,
	'default': DevelopmentConfig
}