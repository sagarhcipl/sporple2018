from forms import query_selectors
from flask_wtf import Form
from wtforms import FileField
from wtforms import TextField
from wtforms import DateField
from wtforms import HiddenField
from wtforms import SelectField
from wtforms import validators
from wtforms.fields.html5 import EmailField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField


def _get_years_experience():
    choices = [(str(x), str(x)) for x in range(1, 10)]
    last_choice = ('10', '10+')
    choices.append(last_choice)
    return choices


class BasicAgentInformationForm(Form):
    firstname = TextField('First Name',
                          [validators.DataRequired()])
    lastname = TextField('Last Name',
                         [validators.DataRequired()])

    profile_agency_image = FileField('Agency Image')
    profile_agency_image_x1 = HiddenField()
    profile_agency_image_y1 = HiddenField()
    profile_agency_image_w = HiddenField()
    profile_agency_image_h = HiddenField()
    profile_agency_rotation = HiddenField()

    user_id = HiddenField()
    user_sport = QuerySelectField('Sport',
            get_label='name',
            blank_text='')
    
    birthday = DateField('Birthday')

    address_country = QuerySelectField('Country',
            get_label='name',
            allow_blank=True,
            query_factory=query_selectors.country)

    address_city = TextField('City')

    nationality = QuerySelectField('Nationality',
            get_label='name',
            allow_blank=True,
            query_factory=query_selectors.nationality)

    agency_name = TextField('Agency')
    agency_url = TextField('Website', [validators.Optional(), validators.URL()])

    years_experience = SelectField('Years experience',
            choices=_get_years_experience())

    def set_form_data(self, profile):
        self.user_sport.data = profile.user.sport


    def update_profile(self, profile):
        self.populate_obj(profile)
        profile.user.sports = [self.user_sport.data]

