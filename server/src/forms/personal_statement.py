from flask_wtf import Form
from wtforms import TextAreaField
from wtforms import validators


class PersonalStatementForm(Form):
    personal_statement = TextAreaField('Personal Statement',
                              [validators.Length(max=2300)])
