from flask_wtf import Form
from forms import query_selectors
from wtforms import SelectField
from wtforms import TextField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import BooleanField


def get_name(obj):
    return obj.name

def get_slug(obj):
    return obj.slug

'''
This form is not validated, this is only used to generate the UI.
'''
class AdvancedSearchForm(Form):
    sports = QuerySelectField('Sport',
        id="sport-select",
        get_pk=get_slug,
        get_label='name',
        query_factory=query_selectors.sport)

    firstname = TextField()
    lastname = TextField()
    clubname = TextField()

    country = QuerySelectField('Country',
        get_pk=get_name,
        get_label='name',
        query_factory=query_selectors.country)

    passport = QuerySelectField('Nationality',
        get_pk=get_name,
        get_label='name',
        blank_text='Choose',
        query_factory=query_selectors.nationality)

    age_min = SelectField(id="min-age-select",
        choices=[('', 'Min')] + [(x,x) for x in range(13,40)])
    age_max = SelectField(id="max-age-select",
        choices=[('', 'Max')] + [(x,x) for x in range(13,40)])

    gender = SelectField(choices=[('male', 'Male'), ('female', 'Female')])

    height_min = SelectField(id="min-height-select",
        choices=[('', 'Min')] + [(x,x) for x in range(100, 245)])
    height_max = SelectField(id="max-height-select",
        choices=[('', 'Max')] + [(x,x) for x in range(100, 245)])

    weight_min = SelectField(id="min-weight-select",
        choices=[('', 'Min')] + [(x,x) for x in range(30, 150)])
    weight_max = SelectField(id="max-weight-select",
        choices=[('', 'Max')] + [(x,x) for x in range(30, 150)])

    has_showreel = BooleanField('Has a showreel')
    has_listings = BooleanField('Has available listings')
    has_agent = BooleanField('Has an agent')
    has_qualifications = BooleanField('Has a qualification listed')
    has_clients = BooleanField('Has a client listed')
    has_vacancies = BooleanField('Has a listing displayed')

    min_experience = SelectField(id="min-experience-select",
        choices=[('', 'Min')] + [(x,x) for x in range(0, 10)])

    # Note: Positions are defined outside of this form.


