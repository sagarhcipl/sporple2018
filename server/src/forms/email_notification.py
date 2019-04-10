from wtforms import BooleanField
from flask_wtf import Form


class EmailNotificationForm(Form):
    new_application = BooleanField()
    new_follower = BooleanField()
    new_post_like = BooleanField()
    new_post_share = BooleanField()
    new_post_message = BooleanField()
    new_message = BooleanField()
    recommendations = BooleanField()
    reminders = BooleanField()
