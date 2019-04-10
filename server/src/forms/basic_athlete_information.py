from forms import query_selectors
from flask_wtf import Form
from wtforms import HiddenField
from wtforms import SelectField
from wtforms import TextField
from wtforms import validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.fields.html5 import DateField
from wtforms.fields.html5 import EmailField


class BasicAthleteInformationForm(Form):
    firstname = TextField('First Name',
                          [validators.DataRequired()])
    lastname = TextField('Last Name',
                         [validators.DataRequired()])

    user_position_list = QuerySelectMultipleField(
            'Positions',
            allow_blank=True,
            blank_text=u'-- please choose --',
            get_label='name')

    birthday = DateField('Birthday')
    height = TextField('Height in cm')
    weight = TextField('Weight in kg')
    address_country = QuerySelectField('Country',
            get_label='name',
            allow_blank=True,
            query_factory=query_selectors.country)
    address_city = TextField('City')
    current_club = TextField('Club')

    nationality = QuerySelectField('Nationality',
            get_label='name',
            allow_blank=True,
            query_factory=query_selectors.nationality)
    passport_1 = QuerySelectField('Nationality',
            get_label='name',
            allow_blank=True,
            query_factory=query_selectors.nationality)
    passport_2 = QuerySelectField('Nationality',
            get_label='name',
            allow_blank=True,
            query_factory=query_selectors.nationality)

    marital_status = QuerySelectField('Marital status',
            get_label='name',
            allow_blank=True,
            query_factory=query_selectors.marital_status)
    children = SelectField('Children',
            choices=[('', ''), ('0', 'No'), ('1', 'Yes')])

    agent_firstname = TextField('Agent First Name')
    agent_lastname = TextField('Agent Last Name')
    agent_email = EmailField('Agent email')


    def set_form_data(self, profile):
        self.user_position_list.data = profile.user.positions

    def update_profile(self, profile):
        self.populate_obj(profile)
        profile.height = self.int_val(self.height.data)
        profile.weight = self.int_val(self.weight.data)
        profile.children = self.bool_val(self.children.data)
        profile.user.positions = [p for p in self.user_position_list.data if p.id]

    def int_val(self, val):
        return int(val) if val else None

    def bool_val(self,val):
        # Could be 0, 1 or None
        if val == '0' or val == 0:
            return False
        if val == '1' or val == 1:
            return True
        return None
