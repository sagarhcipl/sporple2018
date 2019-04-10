from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms.fields import TextAreaField
from wtforms import validators


class PostForm(Form):
    body = TextAreaField()
    filename_0 = FileField(validators=[validators.Optional()])
    filename_1 = FileField(validators=[validators.Optional()])
    filename_2 = FileField(validators=[validators.Optional()])
    filename_3 = FileField(validators=[validators.Optional()])
    filename_4 = FileField(validators=[validators.Optional()])
    filename_5 = FileField(validators=[validators.Optional()])
    filename_6 = FileField(validators=[validators.Optional()])
    filename_7 = FileField(validators=[validators.Optional()])
    filename_8 = FileField(validators=[validators.Optional()])
    filename_9 = FileField(validators=[validators.Optional()])
