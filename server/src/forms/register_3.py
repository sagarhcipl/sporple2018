from forms import query_selectors
from flask_wtf import Form
from wtforms import FileField
from wtforms import HiddenField
from wtforms import SelectField
from wtforms import TextField
from wtforms import validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField


class BaseRegisterStep3(Form):
    image = FileField('Profile pic', validators=[validators.Optional()])
    address_country_id = QuerySelectField('Address Country',
        query_factory=query_selectors.country,
        get_label='name',
        validators=[validators.DataRequired()])
    image_x1 = HiddenField(id='registration_image_x1')
    image_y1 = HiddenField(id='registration_image_y1')
    image_h = HiddenField(id='registration_image_h')
    image_w = HiddenField(id='registration_image_w')
    rotation = HiddenField(id='registration_rotation')
    dd = TextField(validators=[validators.DataRequired()])
    mm = TextField(validators=[validators.DataRequired()])
    yyyy = TextField(validators=[validators.DataRequired()])


class RegisterStepAthlete(BaseRegisterStep3):
    positions = QuerySelectMultipleField('Positions',
        get_label='name',
        validators=[validators.DataRequired()])


EXP_CHOICES = [(str(i), str(i)) for i in range(1, 10)] + [('10', '10+')]
class RegisterStepAgent(BaseRegisterStep3):
    years_experience = SelectField('Years of Experience',
        choices=EXP_CHOICES,
        validators=[validators.DataRequired()])



class RegisterStepClub(BaseRegisterStep3):
    division = TextField('Division', validators=[validators.Optional()])

