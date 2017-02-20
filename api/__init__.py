#!/usr/bin/env python
# Copyright (c) 2016 Jonathan Yantis
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
"""
Flask API Server
"""
import sys
import os
import re
import logging
from logging.handlers import RotatingFileHandler
import configparser
from flask import Flask, jsonify, request, g, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

logger = logging.getLogger(__name__)

# Populated from config file
debug = 1

# Flask Limits for Safety
flask_limits = ["1000 per day", "100 per hour", "5 per minute"]

# Logging Configuration, default level INFO
logger = logging.getLogger('')
logger.setLevel(logging.INFO)
lformat = logging.Formatter('%(asctime)s %(name)s:%(levelname)s: %(message)s')

# Debug mode Enabled
if debug:
    logger.setLevel(logging.DEBUG)
    logging.debug('Enabled Debug mode')

# Enable logging to file if configured
lfh = RotatingFileHandler("api.log", maxBytes=(1048576*5), backupCount=3)
lfh.setFormatter(lformat)
logger.addHandler(lfh)

# STDOUT Logging defaults to Warning
if not debug:
    lsh = logging.StreamHandler(sys.stdout)
    lsh.setFormatter(lformat)
    lsh.setLevel(logging.WARNING)
    logger.addHandler(lsh)

# Create Flask APP
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, "api.db"),
    SQLALCHEMY_DATABASE_URI='sqlite:///' + \
        os.path.join(app.root_path, "api.db"),
    SECRET_KEY='super sexy secrect key, change me!',
    DEBUG = True,
    BCRYPT_LOG_ROUNDS = 4,
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
))

# encryption module
bcrypt = Bcrypt(app)

# Database module
db = SQLAlchemy(app)

# Apply Rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    global_limits=flask_limits
)

# Not Required with SQLAlchemy
# @app.teardown_appcontext
# def close_db(error):
#     """Closes the database again at the end of the request."""
#     db.remove()


# Safe circular imports per Flask guide
import api.errors
import api.views

# auth blueprint
from api.auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)
