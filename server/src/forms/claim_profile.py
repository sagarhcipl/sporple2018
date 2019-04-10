from flask_wtf import Form
from wtforms import TextField
from wtforms import TextAreaField


class ClaimProfile(Form):
    name = TextField('')
    email = TextField('')
    comments = TextAreaField('')

