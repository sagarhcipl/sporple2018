from datetime import datetime
import db
import random
import requests
import string
import urllib
import util
import uuid

from auth import constants
from flask import session
from flask import url_for
from main import app
from main import database as d
from main import sentry
from uploads import upload
from profile import tasks
from etasks import emails


def quick_register(form, user_agent):
    salt, password = util.encrypt_password(form.password.data)
    user = db.User(username=form.email.data, password=password, salt=salt)
    sport = form.sport.data
    if not sport:
        raise UserWarning("Invalid sport")
    role = form.role.data
    if not role:
        raise UserWarning("Invalid role")
    user.sports = [sport]
    d.session.add(user)

    fullname = form.fullname.data.split(' ')
    firstname = fullname[0]
    lastname = ' '.join(fullname[1:]) if len(fullname) > 1 else ''
    clubname = ''
    if role.slug == 'club':
        clubname = form.clubname.data

    profile = db.UserProfile(user=user, device=_max(user_agent), role=role)
    profile.firstname = firstname
    profile.lastname = lastname
    profile.club_name = clubname
    profile.slug = ensure_slug(form.fullname.data)
    gender = form.gender.data
    profile.gender = 0 if gender == 'Male' else 1
    d.session.add(profile)

    _create_user_tables(user)
    d.session.commit()
    return user


def _create_user_tables(user):
    preferences = db.UserEmailPreference(
        user=user,
        new_application=True,
        new_follower=True,
        new_post_like=True,
        new_post_message=True,
        new_post_share=True,
        new_message=True)
    d.session.add(preferences)

    message_user = db.MessageUser(user=user)
    d.session.add(message_user)

    user_login = db.UserLogin(user=user)
    d.session.add(user_login)

def register_info(form, user):
    if form.address_country_id.data:
        user.profile.address_country_id = form.address_country_id.data.id
    dd = int(form.dd.data)
    mm = int(form.mm.data)
    yyyy = int(form.yyyy.data)
    try:
        user.profile.birthday = datetime(yyyy, mm, dd).date()
    except ValueError:
        #sentry.captureException()
        pass

    if form.image.data:
        if form.image_x1.data and form.image_y1.data:
            x1 = int(form.image_x1.data)
            y1 = int(form.image_y1.data)
            w = int(form.image_w.data)
            h = int(form.image_h.data)
            rotation = int(form.rotation.data)

            user.profile.image = upload.s3_resize_and_upload(
                form.image.data,
                x1=x1, y1=y1, w=w, h=h, rotation=rotation,
                sub_dir='/profile')
        else:
            user.profile.image = upload.s3_upload(
                form.image.data, sub_dir='/profile')

    if user.role_slug == 'athlete':
        user.positions = form.positions.data
    elif user.role_slug == 'agent':
        user.profile.years_experience = form.years_experience.data
    elif user.role_slug == 'club':
        user.profile.club_league = form.division.data
        user.profile.slug = ensure_slug(user.name, user.profile.slug)
    d.session.commit()
    tasks.user_registered.delay(user.id)
    if form.image.data:
        tasks.profile_image_uploaded.delay(user.id)


def save_client(form, agent_profile, user_agent):
    username = uuid.uuid4().hex[:15]
    user = db.User(username=username, password=username, salt='')
    profile = db.UserProfile(user=user, device=_max(user_agent))
    profile.role = get_role_from_slug('athlete')
    d.session.add(user)
    d.session.add(profile)
    if form.dd.data and form.mm.data and form.yyyy.data:
        dd = int(form.dd.data)
        mm = int(form.mm.data)
        yyyy = int(form.yyyy.data)
        try:
            profile.birthday = datetime(yyyy, mm, dd).date()
        except ValueError, e:
            sentry.captureException()
 
    fullname = form.name.data.split(' ')
    profile.firstname = fullname[0]
    profile.lastname = ' '.join(fullname[1:]) if len(fullname) > 1 else ''
    profile.current_club = form.club_name.data
    profile.managed_by_id = agent_profile.user_id
    profile.slug = ensure_slug(form.name.data)
    user.sports = [agent_profile.sport]
    try:
        profile.height =  int(form.height.data)
        profile.weight = int(form.weight.data)
    except ValueError,e:
        #sentry.captureException()
        pass
    profile.address_country = form.address_country.data
    if form.position.data:
        user.positions = [form.position.data]

    if form.client_image.data:
        if form.client_image_x1.data and form.client_image_y1.data:
            x1 = int(form.client_image_x1.data)
            y1 = int(form.client_image_y1.data)
            w = int(form.client_image_w.data)
            h = int(form.client_image_h.data)

            profile.image = upload.s3_resize_and_upload(
                    form.client_image.data,
                    x1=x1, y1=y1, w=w, h=h, rotation=0,
                    sub_dir='/profile')
        else:
            profile.image = upload.s3_upload(
                    form.client_image.data,
                    sub_dir='/profile')

    _create_user_tables(user)
    d.session.commit()
    if form.client_image.data:
        tasks.profile_image_uploaded.delay(user.id)
    return profile


def register_unclaimed(form, role='club'):
    username = form.username.data
    password = 'awesomeathlete' # Use same password everywhere
    salt, password = util.encrypt_password(password)
    user = db.User(username=username, password=password, salt=salt)
    profile = db.UserProfile(user=user, device=u'register-unclaimed')
    profile.role = get_role_from_slug(role)
    user.unclaimed = True
    d.session.add(user)
    d.session.add(profile)
    profile.firstname = form.first_name.data
    profile.lastname = form.last_name.data
    if role == 'club':
        profile.slug = ensure_slug(form.club_name.data)
        profile.club_name = form.club_name.data
        profile.club_league = form.club_league.data
        profile.club_contact_url = form.club_contact_url.data
    elif role == 'athlete':
        if form.position.data:
            user.positions = [form.position.data]

    user.sports = [form.sport.data]
    profile.address_country = form.address_country.data

    if form.profile_image.data:
        if form.profile_image_x1.data and form.profile_image_y1.data:
            x1 = int(form.profile_image_x1.data)
            y1 = int(form.profile_image_y1.data)
            w = int(form.profile_image_w.data)
            h = int(form.profile_image_h.data)

            profile.image = upload.s3_resize_and_upload(
                    form.profile_image.data,
                    x1=x1, y1=y1, w=w, h=h, rotation=0,
                    sub_dir='/profile')
        else:
            profile.image = upload.s3_upload(
                    form.profile_image.data,
                    sub_dir='/profile')

    _create_user_tables(user)
    d.session.commit()
    if form.profile_image.data:
        tasks.profile_image_uploaded.delay(user.id)
    return profile


def claim_profile(user_id, form):
    user = db.User.query.get(int(user_id))
    if not user.unclaimed:
        raise UserWarning("Invalid user-id claimed:" + str(user_id))

    claim = db.ClaimProfile(
        user_id=int(user_id),
        email=form.email.data,
        name=form.name.data,
        comments=form.comments.data)
    d.session.add(claim)
    d.session.commit()

    emails.send_claim_request.delay(claim.id)
    return user.profile


def approve_claim(claim_id):
    claim = db.ClaimProfile.query.get(claim_id)
    user = db.User.query.get(claim.user_id)
    user.unclaimed = False
    claim.status = 'approved'
    d.session.commit()
    return user


def invite_friends(user, email_list):
    for email in email_list:
        if email and util.is_valid_email(email):
            invite = db.UserInvite(user_id=user.id, email=email)
            d.session.add(invite)
            emails.invite_friend.delay(email, user.id)
    d.session.commit()


def send_password_reset(user):
    sig = get_password_reset_sig(user.username)
    emails.forgot_password(user.id, sig)    


def get_password_reset_sig(username):
    key = 'D0-#Ff234-@!j5x(ds-' + username
    return util.generate_signature(key)

'''
Return the user if successfully registered / logged in, None otherwise.
'''
def ensure_facebook_register(code, current_url, role_id, sport_id):
    if code:
        url = app.config['FACEBOOK_USER_URL'] % (
                app.config['FACEBOOK_APP_ID'],
                app.config['FACEBOOK_APP_SECRET'],
                urllib.quote(current_url, safe=''),
                code)
        content = requests.get(url)
        if not content.status_code == 200:
            raise UserWarning("Could not validate from facebook")
        params = content.json()
        if params.get('access_token'):
            url = app.config['FACEBOOK_REQUEST_INFO_URL'] % (params['access_token'])
            content = requests.get(url)
            request_params = content.json()
            if request_params and request_params.get('id'):
                return _signin_facebook(request_params, role_id, sport_id)
    return None


def _signin_facebook(params, role_id, sport_id):
    fb_user_id = params.get('id')
    profile = db.UserProfile.query.filter_by(facebook_uid = fb_user_id).first()
    if not profile:
        # TODO(ankit): Why some facebook users don't have email.
        username = params.get('email') or params.get('id')
        user = db.User.query.filter_by(username=username).first()
        if not user:
            if not sport_id or not role_id:
                raise UserWarning("Could not detect sport or role:" +str(sport_id) + str(role_id))

            sport = db.Sport.query.get(int(sport_id))
            role = db.Role.query.get(int(role_id))
            if not sport or not role:
                raise UserWarning("Invalid sport_id or role_id: " + str(sport_id) + str(role_id))
            password = uuid.uuid4().hex[:10]
            salt, password = util.encrypt_password(password)
            user = db.User(username=username, password=password, salt=salt)
            d.session.add(user)
            user.sports = [sport]
            profile = db.UserProfile(
                    user=user,
                    facebook_uid=fb_user_id,
                    password_setup=False,
                    firstname=params.get('first_name'),
                    lastname=params.get('last_name'))
            profile.slug = ensure_slug(profile.firstname + ' ' + profile.lastname)
            profile.role_id = role.id
            if params.get('gender'):
                gender = params.get('gender').lower()
                profile.gender = 0 if gender == 'male' else 1

            if params.get('birthday'):
                try:
                    profile.birthday = datetime.strptime(
                        params.get('birthday'), '%m/%d/%Y')
                except ValueError:
                    pass
            if params.get('location') and params['location'].get('name'):
                location = params['location']['name'].split(',')
                profile.address_city = location[0].strip()
                if len(location) > 1:
                    country_str = location[1].strip()
                    country = db.Country.query.filter_by(name=country_str).first()
                    if country:
                        profile.address_country_id = country.id

            fb_profile_picture_url = 'https://graph.facebook.com/v2.8/' + fb_user_id \
                    + '/picture?type=large&width=200&height=200'

            # Upload to server
            profile.image = upload.s3_upload_from_url(
                    fb_profile_picture_url, sub_dir='/profile')
            d.session.add(profile)
            _create_user_tables(user)
            d.session.commit()
            session['registration_user_id'] = user.id
            session['fb_redirect_url'] = url_for('register_info')

            tasks.profile_image_uploaded.delay(user.id)

        else:
            # User already present
            user.profile.facebook_uid = fb_user_id
            user.profile.firstname = params.get('first_name')
            user.profile.lastname = params.get('last_name')
            d.session.commit()

    else:
        user = profile.user
    return user


def get_role_from_id(id):
    try:
        id = int(id)
    except ValueError:
        return None
    return db.Role.query.get(id)

def get_role_from_slug(slug):
    return db.Role.query.filter_by(slug=slug).first()


def get_sport_from_id(id):
    try:
        id = int(id)
    except ValueError:
        return None
    return db.Sport.query.get(id)


def ensure_slug(name, current_slug=''):
    if not name:
        return current_slug or ''
    base_slug = util.slugify(name)
    if current_slug == base_slug:
        return base_slug
    users = db.UserProfile.query.filter(db.UserProfile.slug.ilike(base_slug + '%')).all()
    if users:
        var = 1 
        slugs = [user.slug for user in users]
        while (base_slug + '-' + str(var)) in slugs:
            var += 1
        return base_slug + '-' + str(var)
    return base_slug


def _max(s, l=200):
    return s if len(s)<=l else s[:l]

def _random_slug():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
