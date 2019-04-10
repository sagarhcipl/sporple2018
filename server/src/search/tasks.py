import db
from main import celery
from main import elasticsearch
from main import sentry

def update_all_users():
    from main import app
    users = db.User.query.filter(db.User.id > 0).all()
    with app.app_context():
        for user in users:
            if user.profile and user.profile.role_id:
                on_register(user.id)
                print "Done", user.id
    print "All Done"


def on_register(user_id):
    user = db.User.query.get(user_id)
    doc = _build_doc(user)
    try:
        res = elasticsearch.index(
            index='users',
            doc_type=user.profile.role.slug,
            id=user.id,
            body={'doc': doc})
    except Exception, e:
        sentry.captureException()
        raise e


def on_update(user_id):
    user = db.User.query.get(user_id)
    doc = _build_doc(user)
    try:
        res = elasticsearch.index(
            index='users',
            doc_type=user.profile.role.slug,
            id=user.id,
            body={'body': doc})
    except Exception, e:
        sentry.captureException()
        raise e


def on_delete(user_id):
    elasticsearch.refresh(index='')
    user = db.User.query.get(user_id)
    try:
        res = elasticsearch.delete(
            index='users',
            doc_type=user.profile.role.slug,
            id=user.id)
    except Exception, e:
        sentry.captureException()
        raise e

def _build_doc(user):
    sports = ', '.join([s.name for s in user.sports_list])
    profile = user.profile
    role = profile.role.slug
    return {
        'firstname':        '' if role == 'club' else profile.firstname,
        'lastname':         '' if role == 'club' else profile.lastname,
        'clubname':         profile.club_name,
        'age':              profile.age,
        'gender':           profile.gender_slug,
        'height':           profile.height,
        'weight':           profile.weight,
        'sports':           sports,
        'positions':        profile.positions_string.replace('/', '-'),
        'city':             _xstr(profile.address_city),
        'country':          _xstr(profile.address_country_slug),
        'passports':        _xstr(profile.passports_slug),
        'avatar':           profile.get_image(),
        'has_showreel':     bool(profile.reel_video_url),
        'showreel_type':    _xstr(profile.reel_video_type),
        'showreel_code':    _xstr(profile.reel_video_url),
        'has_agent':        bool(profile.has_agent),
        'years_of_experience': profile.years_experience,
        'has_qualifications': len(user.qualifications) > 0,
        'has_clients':      len(user.clients) > 0,
        'has_vacancies':    len(user.looking_for_list) > 0,
        'has_listings':     len(user.listings) > 0
    }

# None if empty
def _xstr(string):
    if not string:
        return None
    return string
