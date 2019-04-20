#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import create_app, db
from app.models import Admin
from flask_migrate import Migrate

app = create_app('default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
	return dict(db=db, Admin=Admin)