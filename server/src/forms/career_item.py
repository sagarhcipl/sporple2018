from datetime import date
from forms import query_selectors
from flask_wtf import Form
from wtforms import FileField
from wtforms import HiddenField
from wtforms import SelectField
from wtforms import TextField
from wtforms import TextAreaField


class CareerItemForm(Form):
    club_name = TextField('Club Name')
    team_name = TextField('Team Name')
    location = TextField('Location')
    level = TextField('Level')
    date_from_month = SelectField('', choices=query_selectors.months())
    date_from_year = SelectField('Year', choices=query_selectors.years())
    date_till_month = SelectField('', choices=query_selectors.months())
    date_till_year = SelectField('Year', choices=query_selectors.years())
    item_image = FileField('Image')
    original_image_name = HiddenField('Original Image')
    body = TextAreaField('Body')

    def set_form_data(self, career_item):
        if career_item.date_from:
            self.date_from_month.data = str(career_item.date_from.month)
            self.date_from_year.data = str(career_item.date_from.year)

        if career_item.date_till:
            self.date_till_month.data = str(career_item.date_till.month)
            self.date_till_year.data = str(career_item.date_till.year)

    def update_obj(self, career_item):
        self.populate_obj(career_item)
        if self.date_from_month.data and self.date_from_year.data:
            career_item.date_from = date(
                int(self.date_from_year.data),
                int(self.date_from_month.data),
                1)
        if self.date_till_month.data and self.date_till_year.data:
            career_item.date_till = date(
                int(self.date_till_year.data),
                int(self.date_till_month.data),
                1)

