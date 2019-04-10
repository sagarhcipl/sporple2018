from forms import query_selectors
from flask_wtf import Form
from wtforms import FileField
from wtforms import HiddenField
from wtforms import TextField
from wtforms import validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import EmailField


class BasicClubInformationForm(Form):
    club_name = TextField('Club',
                          [validators.DataRequired()])
    club_contact_url = TextField('Website',
                          [validators.Optional()])

    year_establishment = TextField('Year of Establishment')
    club_league = TextField('Division')

    profile_image = FileField('image File')
    profile_image_x1 = HiddenField()
    profile_image_y1 = HiddenField()
    profile_image_x2 = HiddenField()
    profile_image_y2 = HiddenField()
    profile_image_w = HiddenField()
    profile_image_h = HiddenField()
    profile_rotation = HiddenField()
    user_id = HiddenField()

    address_country = QuerySelectField('Country',
            get_label='name',
            allow_blank=True,
            query_factory=query_selectors.country)
    address_city = TextField('City')


