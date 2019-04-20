#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from . import auth
from .forms import LoginForm
from ..models import Admin

@auth.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
        	admin = Admin.query.filter_by(name=form.name.data).first()
        	if admin.verify_password(form.password.data):
        		login_user(admin)
        		return render_template('manage_index.html')
        	else:
        		flash('密码错误！')
        		return redirect(url_for('auth.login'))
        else:
        	flash('登陆失败！')
        	return redirect(url_for('auth.login'))
    else:
        return render_template('auth/login_index.html', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.login'))