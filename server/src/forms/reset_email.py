from flask_wtf import Form
from wtforms import PasswordField
from wtforms import validators
from wtforms.fields.html5 import EmailField


class ResetEmailForm(Form):
    current_password = PasswordField('',
            validators=[validators.DataRequired()])
    email = EmailField('', validators=[validators.DataRequired()])

