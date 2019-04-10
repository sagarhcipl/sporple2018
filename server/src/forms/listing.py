from flask_wtf import Form
from wtforms import IntegerField
from wtforms import TextField
from wtforms import TextAreaField
from wtforms import validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.fields.html5 import DateField


class ListingForm(Form):
    description = TextAreaField('Description')
    season_start = DateField('Season Start')
    position = QuerySelectField('Position', get_label='name')
    age_min = IntegerField('Age Min', [
            validators.Optional(),
            validators.NumberRange(0, 99)], default='0')
    age_max = IntegerField('Age Max', [
            validators.Optional(),
            validators.NumberRange(0, 99)], default='99')
    height_min = IntegerField('Height Min', [
            validators.Optional(),
            validators.NumberRange(0, 999)], default='0')
    height_max = IntegerField('Height Max', [
            validators.Optional(),
            validators.NumberRange(0, 999)], default='999')
    weight_min = IntegerField('Weight Min', [
            validators.Optional(),
            validators.NumberRange(0, 999)], default='0')
    weight_max = IntegerField('Weight Max', [
            validators.Optional(),
            validators.NumberRange(0, 999)], default='999')
    country_groups = QuerySelectMultipleField('Allowed Passports', get_label='name')


    def set_form_data(self, listing):
        if listing:
            self.position.data = listing.position

