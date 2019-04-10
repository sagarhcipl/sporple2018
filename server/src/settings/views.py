import db
import util

from flask.ext.login import login_required
from flask.ext.login import current_user
from flask import render_template
from flask import request
from forms.email_notification import EmailNotificationForm
from forms.reset_password import ResetPasswordForm
from forms.reset_email import ResetEmailForm
from main import database as d


@login_required
def email_notifications():
    email_preference = (db.UserEmailPreference.query
        .filter_by(user_id=current_user.user.id).first())
    if not email_preference:
        email_preference = db.UserEmailPreference(
                user=current_user.user,
                new_application=True,
                new_follower=True,
                new_post_like=True,
                new_post_message=True,
                new_post_share=True,
                new_message=True)
        d.session.add(email_preference)
        d.session.commit()
    form = EmailNotificationForm(request.form, obj=email_preference)
    success_message = ''
    if request.method == 'POST' and form.validate():
        form.populate_obj(email_preference)
        d.session.commit()
        success_message = 'Your email preferences have been changed successfully!'
    return render_template('forms/email_notifications.html', form=form, success_message=success_message)

@login_required
def password():
    has_password = current_user.user.profile.password_setup
    form = ResetPasswordForm(request.form)

    success_message = ''
    if request.method == 'POST' and form.validate():
        if has_password:
            # Make sure the current_password is valid
            encrypted_password = util.encrypt_password(
                form.current_password.data, current_user.user.salt)
            if encrypted_password != current_user.user.password:
                form.current_password.errors.append('Invalid password')
                return render_template('forms/reset_password.html',
                    form=form, has_pasword_setup=True)
        salt, password = util.encrypt_password(form.password.data)
        current_user.user.password = password
        current_user.user.salt = salt
        current_user.user.profile.password_setup = True
        d.session.commit()

        # Reset form
        form = ResetPasswordForm()
        success_message = 'Your password has been changed successfully !'
    return render_template('forms/reset_password.html', form=form, success_message=success_message, has_password_setup=has_password)


@login_required
def email():
    has_password_setup = current_user.user.profile.password_setup
    form = ResetEmailForm(request.form)
    success_message = ''
    if request.method == 'POST' and form.validate():
        if has_password_setup:
            encrypted_password = util.encrypt_password(
                form.current_password.data, current_user.user.salt)
            if encrypted_password != current_user.user.password:
                form.current_password.errors.append('Invalid password')
                return render_template('forms/reset_email.html',
                    form=form, has_password_setup=has_password_setup)

        if current_user.user.username != form.email.data  \
            and db.User.query.filter_by(username=form.email.data).first():
            form.email.errors.append("The email already exist")
        else:
            current_user.user.username = form.email.data
            d.session.commit()

            # Reset form
            form = ResetEmailForm()
            success_message = 'Your email has been changed successfully!'
    return render_template('forms/reset_email.html', form=form, success_message=success_message, has_password_setup=has_password_setup)


