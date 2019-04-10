from flask_wtf import Form
from wtforms import TextAreaField
from wtforms import validators

class ApplicationForm(Form):
    note = TextAreaField(validators=[validators.Optional()])
