#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint

order = Blueprint('order', __name__)

from . import views