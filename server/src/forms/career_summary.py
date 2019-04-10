from flask_wtf import Form
from wtforms import TextAreaField
from wtforms import validators


class CareerSummaryForm(Form):
    career_summary = TextAreaField('Career Summary',
                              [validators.Length(max=2300)])
