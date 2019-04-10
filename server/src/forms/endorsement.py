from datetime import date
from flask_wtf import Form
from wtforms import SelectField
from wtforms import TextField
from wtforms import TextAreaField

class EndorsementForm(Form):
    first_name = TextField('First Name')
    last_name = TextField('Last Name')
    body = TextAreaField('Body')
    title = TextField('Title')
    month = SelectField('Month', choices = [(str(x), x) for x in range(1, 12)])
    year = SelectField('Year', choices=[(str(x), x) for x in reversed(range(1950, date.today().year))])

    def set_form_data(self, endorsement):
        if endorsement.date:
            self.month.data = str(endorsement.date.month)
            self.year.data = str(endorsement.date.year)

    def update_obj(self, endorsement):
        self.populate_obj(endorsement)
        if self.month.data and self.year.data:
            endorsement.date = date(int(self.year.data), int(self.month.data), 1)
