from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import HiddenField


class ProfileImageForm(Form):
    profile_image = FileField('Image File')
    profile_image_x1 = HiddenField()
    profile_image_y1 = HiddenField()
    profile_image_w = HiddenField()
    profile_image_h = HiddenField()
    profile_rotation = HiddenField()


