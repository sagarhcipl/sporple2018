#!/usr/bin/python

import config
import datetime
import htmlentitydefs
import jinja2
import re
import os
import random
import string
import traceback
from config import sport
from celery import Celery
from flask import Flask
from flask import abort
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask.ext.login import LoginManager
from flask.ext.login import current_user
from flask.ext.session import Session
from flask.ext.sqlalchemy import SQLAlchemy
from redis import Redis
from user.current_user import CurrentUser
from user.current_user import Anonymous

'''
The main application setup. The order of things is important
in this file.
'''
app = Flask(__name__)
app.config.from_object('config.base')
app.config.from_envvar('APP_CONFIG_FILE')
app.config.from_pyfile('../config/autogen.py')
app.config['APP_ROOT'] = os.path.dirname(os.path.abspath(__file__))
app.config['ENVIRONMENT'] = os.environ.get('ENVIRONMENT', 'dev')
app.config['SERVER_NAME'] = os.environ.get('SERVER_NAME', 'local.sporple.com')


'''
Initialize serverside sessions.
'''
app.config['SESSION_REDIS'] = Redis(app.config['SESSION_REDIS_HOST'], port=6379, db=1)
Session(app)

'''
Initialize database
'''
database = SQLAlchemy(app)


'''
Initialize models. This import makes sure all the models
are defined and parsed by SQL Alchemy.
'''
import db

'''
Initialize sentry and enable logging.
'''
import logging
from raven.contrib.flask import Sentry
sentry = Sentry(app, logging=True, level=logging.ERROR,
    dsn=app.config['SENTRY_DSN'])

logging.getLogger().setLevel(logging.INFO)
if app.config.get('ENVIRONMENT') != 'dev':
    from logging.handlers import TimedRotatingFileHandler
    logging_handler = TimedRotatingFileHandler(
        '/data/log/webapp/app.log',
        when='W1', # Rotate every Tuesday
        utc=True)
    logging_handler.setLevel(logging.INFO)
    app.logger.addHandler(logging_handler)
    logging.getLogger().addHandler(logging_handler)
else:
    logging.getLogger().addHandler(logging.StreamHandler())
# Test logging
logging.info("Starting Logger:" + app.config.get('SERVER_NAME', ''))



'''
Initialize the login manager
'''
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous
login_manager.login_view = 'signin'

@login_manager.user_loader
def load_user(userid):
    user = db.User.query.get(userid)
    if user:
        return CurrentUser(user)
    return None



'''
Initialize Elasticsearch Extension.
'''
from flask.ext.elasticsearch import FlaskElasticsearch
elasticsearch = FlaskElasticsearch(app)


'''
Initialize braintree
'''
import braintree
payment_env = braintree.Environment.Sandbox if app.config['DEBUG'] \
                else braintree.Environment.Production
braintree.Configuration.configure(payment_env,
        merchant_id=app.config['BRAINTREE_MERCHANT_ID'],
        public_key=app.config['BRAINTREE_PUBLIC_KEY'],
        private_key=app.config['BRAINTREE_PRIVATE_KEY'])


'''
Initialize Flask-Celery for background tasks.
'''
from celery import Celery

def make_celery(app):
    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                response = TaskBase.__call__(self, *args, **kwargs)
                return response

        def on_retry(self, exc, task_id, args, kwargs, einfo):
            """Log the exceptions to sentry at retry."""
            logging.error(str(exc))
            sentry.captureMessage("[retry]Backend exception: " + str(exc), extra={
                    'traceback': traceback.format_tb(einfo.tb)
            })
            super(ContextTask, self).on_retry(exc, task_id, args, kwargs, einfo)

        def on_failure(self, exc, task_id, args, kwargs, einfo):
            """Log the exceptions to sentry."""
            logging.error(str(exc))
            sentry.captureMessage("[failure]Backend exception: " + str(exc), extra={
                    'traceback': traceback.format_tb(einfo.tb)
            })
            super(ContextTask, self).on_failure(exc, task_id, args, kwargs, einfo)


    celery.Task = ContextTask
    return celery

celery = make_celery(app)


'''
Initialize all views so that all the route are set correctly.
'''
from main import urls


'''
Initialize flask request variables
'''
from main import base

@app.errorhandler(404)
def page_not_found(e):
    sentry.captureMessage("Page not found",
            extras={
                'url': request.url,
                'referrer': request.referrer
    })
    return render_template('error404Success.html'), 404


'''
Flask template filters
'''
@app.template_filter('escape_quote')
def escape_quote(val):
    return val.replace("\"", "&quot;")

@app.template_filter('nl2br')
def nl2br(string):
    return string.replace('\n','<br />\n')

escaped_pattern = re.compile("&(\w+?);")
hyperlink_regex = re.compile(r'(|http)(|s)(|://)(([-\w]+\.)+([^\s]+)+[^,.\s])')
@app.template_filter('link_text')
def link_text(string):
    if not string:
        return ''
    string = string.encode('ascii', 'ignore')
    string = str(jinja2.escape(string))
    match = hyperlink_regex.search(string)
    string = hyperlink_regex.sub(r'<a target="_blank" href="http\2://\4">\1\2\3\4</a>', string)
    return jinja2.Markup(string.replace('\n', '<br/>\n'))

@app.template_filter('html_entity_decode')
def html_entity_decode(val):
    return escaped_pattern.sub(_html_entity_decode_char, val)

def _html_entity_decode_char(m, defs=htmlentitydefs.entitydefs):
    try:
        return defs[m.group(1)]
    except KeyError:
        return m.group(0)

@app.template_filter('escape_custom')
def escape_custom(string):
    if not string:
        return ''
    string = string.encode('ascii', 'ignore')
    string = str(jinja2.escape(string))
    return jinja2.Markup(string.replace('\n', '<br/>\n'))

@app.template_filter('format_price_cents')
def format_price_cents(val):
    return "{0:.2f}".format(val / 100)

