import db
from mailchimp import Mailchimp
from main import app
from main import celery
from main import sentry


@celery.task()
def subscribe_user(user_id):
    user = db.User.query.get(user_id)
    if '@' not in user.username:
        return
    client = Mailchimp(app.config['MAILCHIMP_API_KEY'])

    agent_list_id = '9cc300951b'
    athlete_list_id = '1837caaaf7'
    club_list_id = '4daa496bdd'
    list_id = 'b9462f3927'

    profile = user.profile
    role_slug = profile.role.slug
    if role_slug == 'agent':
        list_id = agent_list_id
    elif role_slug == 'athlete':
        list_id = athlete_list_id
    elif role_slug == 'club':
        list_id = club_list_id
    else:
        raise RuntimeError("Invalid role for user:" + str(user_id))

    if not app.config['MAILCHIMP_SYNC_ENABLED']:
        list_id = '3a5cf93572'

    merge_vars = {
        'FNAME': profile.firstname,
        'LNAME': profile.lastname,
        'ROLE': role_slug,
        'BIRTHDAY': profile.birthday.strftime('%Y-%m-%d') if profile.birthday else '',
        'GENDER': profile.gender_slug,
        'SPORT': user.sport_slug,
        'CLUB_NAME': profile.club_name or '',
        'CUR_CLUB': profile.current_club,
        'CUR_TEAM': profile.current_team,
        'CUR_DIV': profile.current_division,
        'HAS_AGENT': profile.has_agent,
        'EXP_YEARS': profile.years_experience,
        'NATIONAL': profile.nationality_slug,
        'CUR_COUNT': profile.address_country_slug,
        'CUR_CITY': profile.address_city,
        'OCCUPATION': profile.occupation,
        'HAS_VIDEO': _b(profile.reel_video_url),
        'HAS_AVATAR': _b(profile.image),
        'IS_MM': _b(profile.midnight_madness),
        'CAREER_SUM': _b(profile.career_summary),
        'PERS_STAT': _b(profile.personal_statement),
        'CAREER_ENT': _b(profile.user.career_items),
        'HAS_LIST': _b(profile.user.listings),
        'URL': app.config['BASE_URL'] + '/' + profile.slug,
    }

    try:
        client.lists.subscribe(list_id, {'email': user.username},
            merge_vars = merge_vars, double_optin=False, update_existing=True)
    except Exception, e:
        sentry.captureException()


def _b(val):
    return 'Yes' if val else 'No'
