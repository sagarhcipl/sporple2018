from datetime import date
from flask_wtf import Form
from wtforms import SelectField
from wtforms import TextField
from wtforms import TextAreaField

class AchievementForm(Form):
    year = SelectField('Year', choices=[(str(x), x) for x in reversed(range(1950, date.today().year))])
    title = TextField('Title')
    summary = TextAreaField('Summary')
