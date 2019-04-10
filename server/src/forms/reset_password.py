from flask_wtf import Form
from wtforms import PasswordField
from wtforms import validators


class ResetPasswordForm(Form):
    password = PasswordField('',
            validators=[validators.DataRequired(),
                        validators.Length(min=6, max=50)])

    password_confirm = PasswordField('',
            validators=[validators.DataRequired(),
                        validators.Length(min=6, max=50)])

    current_password = PasswordField()

    def validate(self, forgot=False):
        if not Form.validate(self):
            return False
        if not forgot and not self.current_password.data:
            self.current_password.errors.append('Current password is required')
        if self.password.data != self.password_confirm.data:
            self.password_confirm.errors.append('Passwords do not match.')
            return False
        return True
