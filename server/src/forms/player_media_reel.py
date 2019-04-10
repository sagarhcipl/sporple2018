from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import HiddenField
from wtforms import TextField


class PlayerMediaReelForm(Form):
    reel_video_url =  TextField()
    reel_image = FileField()
    reel_image_x1 = HiddenField()
    reel_image_y1 = HiddenField()
    reel_image_x2 = HiddenField()
    reel_image_y2 = HiddenField()
    reel_image_w = HiddenField()
    reel_image_h = HiddenField()
    is_temp = HiddenField()


