import logging
import re
import urllib
import util

from auth import controller
from config import cache
from auth import constants
from db import User
from db import UserProfile
from forms import query_selectors
from forms.auto_register import AutoRegisterClub
from forms.claim_profile import ClaimProfile
from forms.quick_register import QuickRegisterForm
from forms.register_1 import RegisterStep1
from forms.register_3 import RegisterStepAthlete
from forms.register_3 import RegisterStepAgent
from forms.register_3 import RegisterStepClub
from forms.reset_password import ResetPasswordForm
from flask import abort
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask.ext.login import current_user
from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.login import logout_user
from main import app
from main import database as d
from main import sentry
from urlparse import urljoin
from urlparse import urlparse
from user.current_user import CurrentUser



def login():
    next_page = request.form.get('next', '')
    if not _is_safe_url(next_page):
        next_page = ''

    if current_user.is_authenticated:
        redirect_url = next_page or url_for('profile.slug', slug=current_user.user.slug)
        return jsonify(loggedIn=True, redirectUrl=redirect_url)

    username = request.form.get('signin[username]', '').strip()
    password = request.form.get('signin[password]', '').strip()

    user = User.query.filter_by(username=username).first()
    remember = 'signin[remember]' in request.form
    if user and util.encrypt_password(password, user.salt) == user.password \
        and user.id != 4892:
        _login_user(user, remember)
        redirect_url = next_page or url_for('profile.slug', slug=user.slug)
        return jsonify(loggedIn=True, redirectUrl=redirect_url)
    else:
        return jsonify(loggedIn=False, error='Invalid Email/Password')


def login_page():
    next_page = request.args.get('next', '')
    if not _is_safe_url(next_page):
        next_page = ''
    if current_user.is_authenticated:
        redirect_url = next_page or url_for('profile.slug', slug=current_user.user.slug)
        return redirect(redirect_url)

    return render_template('forms/login.html')


@login_required
def login_as(slug):
    if not current_user.user.is_super_admin:
        abort(404)
    profile = UserProfile.query.filter_by(slug=slug).first()
    if not profile:
        abort(404)

    _login_user(profile.user)
    return redirect(url_for('profile.slug', slug=profile.slug))


def logout():
    logout_user()
    return redirect(url_for('index'))


def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    username = request.form.get('username', '').strip()
    success = False
    error = False
    if username:
        user = User.query.filter_by(username=username).first()
        if user:
            controller.send_password_reset(user)
            success='Password reset instructions sent on email.'
        else:
            error='Cannot find email.'

    if request.is_xhr:
        return jsonify(success=bool(success), error=error)

    return render_template('auth/forgot_password.html', success=success, error=error)


def reset_password():
    username = request.args.get('username', '')
    sig = request.args.get('sig', '')
    if not username or sig != controller.get_password_reset_sig(username):
        return redirect(url_for('index'))

    user = User.query.filter_by(username=username).first()
    _login_user(user)

    params = {}
    form = ResetPasswordForm(request.form)
    params['has_password_setup'] = user.profile.password_setup
    if request.method == 'POST' and form.validate(forgot=True):
        salt, password = util.encrypt_password(form.password.data)
        user.password = password
        user.salt = salt
        user.profile.password_setup = True
        d.session.commit()

        form = ResetPasswordForm()
        success_message = 'Your password has been changed successfully !'
        params['success_message'] = success_message

    params['form'] = form
    params['forgot_password'] = True
    return render_template('forms/reset_password.html', **params)


def _password_reset_sig(username):
    key = 'D0-#Ff234-@!j5x(ds-' + username
    return  util.generate_signature(key)

def change_password():
    return render_template('auth/change_password.html')


def facebook_authorize():
    code = request.args.get('code')
    error = request.args.get('error')

    # Facebook crawler workaround
    user_agent = request.headers.get('User-Agent')
    is_facebook_crawler = re.search('/facebookexternalhit/i', user_agent)
    logging.info('user-agent:' + user_agent)
    logging.info('is facebook crawler:', + bool(is_facebook_crawler))

    if is_facebook_crawler:
        return 'hello Facebook!'

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    elif error:
        return abort(404)
    elif code:
        role = session.pop('role_id', None)
        sport = session.pop('sport_id', None)
        try:
            user = controller.ensure_facebook_register(code, request.base_url, role, sport)
        except UserWarning:
            return redirect(url_for('register'))
        if user:
            _login_user(user)
            if session.get('fb_redirect_url'):
                return redirect(session.pop('fb_redirect_url', None))
            else:
                return redirect(url_for('profile.slug', slug=user.profile.slug))
        else:
            return ''

    else:
        # Generate facebook url
        current_url = url_for('facebook_authorize', _external=True)
        return_url = request.args.get('next') or \
            request.referrer or \
            url_for('home')
        session['return_url'] = return_url
        session['role_id'] = request.form.get('role')
        session['sport_id'] = request.form.get('sport')

        url = app.config['FACEBOOK_OAUTH_URL'] % (
            app.config['FACEBOOK_APP_ID'],
            urllib.quote(current_url, safe=''),
            ','.join(app.config['FACEBOOK_APP_PERMISSIONS']))

        if request.is_xhr:
            return jsonify(success=True, redirectUrl=url)
        else:
            return redirect(url)


def registration_congratulations():
    _pre_congratulations()
    return render_template('auth/registration_congratulations.html')


def register(sport=None):
    form = QuickRegisterForm()
    return render_template('auth/register.html', form=form, hide_container=True)


def register_json():
    form = QuickRegisterForm()
    if request.method == 'POST' and form.validate():
        user = controller.quick_register(form, request.headers.get('User-Agent'))
        session['registration_user_id'] = user.id
        redirect_url = url_for('register_info')
        return jsonify(registerSuccess=True, redirectUrl=redirect_url)
    else:
        return jsonify(registerSuccess=False)


def register_info():
    params = {}
    user_id = int(session.get('registration_user_id', 0))
    if not user_id:
        return redirect(url_for('register'))

    user = User.query.get(user_id)
    role = user.role_slug
    params['user'] = user
    params['role'] = role
    if role == 'athlete':
        params['form'] = RegisterStepAthlete()
        params['form'].positions.query = query_selectors.user_position_list(user.sport.id)

    elif role == 'agent':
        params['form'] = RegisterStepAgent()
    elif role == 'club':
        params['form'] = RegisterStepClub()

    if request.method == 'POST' and params['form'].validate():
        controller.register_info(params['form'], user)
        return redirect(url_for('registration_congratulations'))
    else:
        return render_template('auth/register_info.html', **params)


def auto_register_club():
    form = AutoRegisterClub()
    club_name = None
    slug = None
    if request.method == 'POST' and form.validate():
        profile = controller.register_unclaimed(form, role='club')
        club_name = form.club_name.data
        slug = profile.slug
        form = AutoRegisterClub(formdata=None)
    return render_template('forms/auto_register_club.html', form=form, club_name=club_name, slug=slug)


def claim_profile(user_id):
    form = ClaimProfile()
    if request.method == 'POST' and form.validate():
        profile = controller.claim_profile(user_id, form)
        return render_template('profile/claim_submitted.html', email=form.email.data)

    return render_template('forms/claim_profile.html', form=form, user_id=user_id)


@login_required
def approve_claim(claim_id):
    if not current_user.user.is_super_admin:
        abort(404)
    user = controller.approve_claim(claim_id)
    profile_url = url_for('profile.slug', slug=user.slug)
    return "Claim Approved for " + user.name + ". <a href='" + profile_url + "'>View Profile</a>"


@login_required
def invite_friends():
    success = False
    if request.method == 'POST':
        email_list = request.form.getlist('emails[]')
        controller.invite_friends(current_user.user, email_list)
        success = True
    return render_template('forms/invite.html', success=success)


def auto_register_athlete():
    form = AutoRegisterAthlete()
    return render_template('forms/auto_register_athlete.html', form=form)

# Helper methods
def _login_user(user, remember=True):
    logged_in_user = CurrentUser(user)
    login_user(logged_in_user, remember=remember)


def _pre_congratulations():
    user_id = session.pop('registration_user_id', None)
    if user_id:
        user = User.query.get_or_404(user_id)
        _login_user(user)
    elif not current_user.is_authenticated:
        sentry.captureMessage("No registered_user for referrer:" + str(request.referrer))
        abort(403)


def _is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
