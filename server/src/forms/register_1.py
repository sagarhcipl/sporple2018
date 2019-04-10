from flask_wtf import Form
from wtforms import RadioField
from wtforms import PasswordField
from wtforms import TextField
from wtforms import validators
from wtforms.fields.html5 import DateField
from wtforms.fields.html5 import EmailField


class RegisterStep1(Form):
    first_name = TextField('Firstname',
            validators=[validators.DataRequired(), validators.length(max=50)])
    
    last_name = TextField('LastName',
            validators=[validators.DataRequired(), validators.length(max=50)])

    gender = RadioField('Gender',
            choices=[('male', 'Male'), ('female', 'Female')],
            default='male',
            validators=[validators.DataRequired()])

    birthday = DateField('Birthday',
            validators=[validators.DataRequired()])

    username = EmailField('Email',
            validators=[
                validators.Optional(),
                validators.Email()])

    password = PasswordField('Password')

