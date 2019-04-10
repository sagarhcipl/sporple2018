import datetime
from flask_wtf import Form
from wtforms import SelectField
from wtforms import TextField
from wtforms.fields import TextAreaField
from wtforms import validators


class QualificationForm(Form):
    title = TextField(validators=[validators.DataRequired()])
    year = SelectField(choices=[(str(x), x) for x in reversed(range(1950, datetime.date.today().year + 5))])
    summary = TextAreaField()

