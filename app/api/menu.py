#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from flask import jsonify, request, Response
from . import api
from ..models import Menu

@api.route('/menus/')
def get_menus():
	menu_type = request.args.get('menu_type')
	if request.args.get('count'):
		count = int(request.args.get('count'))
		menus = Menu.query.filter_by(type_name=menu_type, is_grounding=True).order_by(Menu.id.desc()).all()[0:count]
	else:
		menus = Menu.query.filter_by(type_name=menu_type, is_grounding=True).order_by(Menu.id.desc()).all()
	return jsonify({'menus': [menu.to_json() for menu in menus]})

@api.route('/menus/<int:id>')
def get_menu(id):
	menu = Menu.query.get_or_404(id)
	return jsonify(menu.to_json())
