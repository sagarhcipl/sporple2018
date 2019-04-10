from forms import query_selectors
from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import HiddenField
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import TextField
from wtforms.ext.sqlalchemy.fields import QuerySelectField


class ClientForm(Form):
    client_image = FileField()
    client_image_x1 = HiddenField()
    client_image_y1 = HiddenField()
    client_image_x2 = HiddenField()
    client_image_y2 = HiddenField()
    client_image_w = HiddenField()
    client_image_h = HiddenField()

    name = TextField()
    club_name = TextField()
    height = IntegerField()
    weight = IntegerField()
    dd = IntegerField()
    mm = SelectField(choices=query_selectors.months())
    yyyy = SelectField(choices=query_selectors.years())
    position = QuerySelectField('Position', get_label='name')
    address_country = QuerySelectField('Country',
            get_label='name',
            allow_blank=True,
            query_factory=query_selectors.country)


