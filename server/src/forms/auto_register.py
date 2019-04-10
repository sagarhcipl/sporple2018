from db import User
from forms import query_selectors
from flask_wtf import Form
from wtforms import FileField
from wtforms import HiddenField
from wtforms import TextField
from wtforms import validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.fields.html5 import DateField
from wtforms.fields.html5 import EmailField


def unique_username(form, field):
    if User.query.filter_by(username=field.data).first():
        raise validators.ValidationError('The email already exist')

'''
Registration Form for unclaimed profiles
'''
class AutoRegister(Form):
    first_name = TextField('Firstname',
            validators=[validators.DataRequired(), validators.length(max=50)])
    
    last_name = TextField('LastName',
            validators=[validators.DataRequired(), validators.length(max=50)])

    username = EmailField('Email',
            validators=[
                validators.Optional(),
                validators.Email(),
                unique_username])

    sport = QuerySelectField('', query_factory=query_selectors.sport,
        get_label='name',
        validators=[validators.DataRequired()])

    profile_image = FileField('', validators=[validators.Optional()])

    profile_image_x1 = HiddenField()
    profile_image_y1 = HiddenField()
    profile_image_x2 = HiddenField()
    profile_image_y2 = HiddenField()
    profile_image_w = HiddenField()
    profile_image_h = HiddenField()
    profile_rotation = HiddenField()

    address_country = QuerySelectField('', query_factory=query_selectors.country, get_label='name')
    address_city = TextField('', validators=[validators.Optional()])


class AutoRegisterClub(AutoRegister):
    club_league = TextField('', validators=[validators.Optional()])
    club_contact_url = TextField('', validators=[validators.Optional()])
    club_name = TextField('',
            validators=[validators.DataRequired(), validators.length(max=200)])

class AutoRegisterAthlete(AutoRegister):
    dd = TextField(validators=[validators.DataRequired()])
    mm = TextField(validators=[validators.DataRequired()])
    yyyy = TextField(validators=[validators.DataRequired()])

    positions = QuerySelectMultipleField('', get_label='name')

