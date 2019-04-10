from db import User
from forms import query_selectors
from flask_wtf import Form
from wtforms import PasswordField
from wtforms import RadioField
from wtforms import TextField
from wtforms import validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import EmailField

from sqlalchemy import text
from main import database as d

def unique_username(form, field):
    email = field.data
    # Prevents gmail users from duplicating email addresses
    # e.g. andrew@gmail.com == and.rew@gmail in Google's eyes
    if '@gmail.com' in email:
        json = []
        name = email[0:len(email)-10].replace('.', '')
        sql = text("select * from sf_guard_user where username like '%@gmail.com' and REPLACE(REPLACE(username,'@gmail.com',''),'.','') = '" + name + "'");

        data = d.engine.execute(sql)

        for item in data:
            print item.username
            json.append(item.username)

        if json:
            raise validators.ValidationError('The email already exist')
    else:
        if User.query.filter_by(username=field.data).first():
            raise validators.ValidationError('The email already exist')


def required(form, field):
    if not field.data:
        raise validators.ValidationError('Value is required')


class QuickRegisterForm(Form):
    sport = QuerySelectField('Sport',
            query_factory=query_selectors.sport,
            get_label='name',
            allow_blank=True,
            blank_text=u'Choose Your Sport',
            validators=[required])

    role = QuerySelectField('Role',
            query_factory=query_selectors.role,
            get_label='name',
            allow_blank=True,
            blank_text=u'Choose Your Profile',
            validators=[required])

    email = EmailField('Email Address', validators=[
        validators.DataRequired(),
        validators.Email(),
        unique_username])

    password = PasswordField('Create Password', validators=[
        validators.DataRequired()])

    fullname = TextField('', validators=[
        validators.DataRequired()])

    clubname = TextField('', validators=[
        validators.Optional()])

    gender = RadioField('Gender',
            choices=[('Male', 'Male'), ('Female', 'Female')],
            default='Male',
            validators=[validators.DataRequired()])

