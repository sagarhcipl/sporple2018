from forms import query_selectors
from flask_wtf import Form
from wtforms import SelectField

from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField


class SearchOpportunity(Form):
    country = QuerySelectMultipleField('', get_label='name')

    positions = QuerySelectMultipleField('', get_label='name')
    # TODO(ankit): Filter by season dates
