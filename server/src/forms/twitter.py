from flask import session
from flask_wtf import Form
from wtforms import TextField
from wtforms import validators


class TwitterForm(Form):
    twitter_account = TextField('Twitter username',
                                [validators.DataRequired()])
