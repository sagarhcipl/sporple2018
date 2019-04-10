from flask_wtf import Form
from wtforms import TextAreaField


class ClubAboutForm(Form):
    career_summary = TextAreaField()
