import datetime
import re
import soundcloud
import util
from config import image_sizes
from main import app
from flask import session
from flask.ext.login import current_user
from forms.quick_register import QuickRegisterForm

@app.context_processor
def inject_params():
    params = {}
    params['title'] = app.config['BASE_TITLE']
    params['now'] = datetime.datetime.utcnow()
    params['sport'] = ''
    if current_user and current_user.is_authenticated and current_user.user.sport:
        params['sport'] = current_user.user.sport.slug
    for key in app.config:
        params[key] = app.config[key]

    params['use_stylesheet'] = use_stylesheet
    params['use_javascript'] = use_javascript
    params['image_path'] = image_path
    params['post_date_format'] = post_date_format
    params['replace_media_links'] = replace_media_links
    params['avatar'] = avatar

    if current_user and not current_user.is_authenticated:
        params['qr_form'] = QuickRegisterForm()

    # One time hack for setting people properties in mixpanel.
    if current_user and current_user.is_authenticated \
            and current_user.user.role_slug \
            and not session.get('mixpanel_version'):
        session['mixpanel_version'] = 1
        params['set_new_mixpanel_props'] = True

    return params

def use_stylesheet(path):
    return ('<link rel="stylesheet" type="text/css" media="screen"'
        + ' href="' + app.config['STATIC_CONFIG_PATH'] + 'css/' + path
        + '?' + app.config['VERSION_ID']
        + '" />')


def use_javascript(path):
    return ('<script type="text/javascript" src="'
        + app.config['STATIC_CONFIG_PATH'] + 'js/' + path
        + '?' + app.config['VERSION_ID']
        + '"></script>')


def image_path(path, external=False):
    base_url = app.config['STATIC_CONFIG_PATH'] + 'images/'
    if external:
        base_url = app.config['BASE_URL'] + base_url
    return base_url + path

def avatar(path, size):
    return image_sizes.get_resized(path, size)


def post_date_format(time):
    return util.pretty_date(time)


def replace_media_links(string):
    youtube_regex = re.compile(r"""
        # Match youtube URLs.
        https?://         # Required scheme. Either http or https.
        (?:[0-9A-Z-]+\.)? # Optional subdomain.
        (?:               # Group host alternatives.
          youtu\.be/      # Either youtu.be,
        | youtube         # or youtube.com or
          (?:-nocookie)?  # youtube-nocookie.com
          \.com           # followed by
          \S*             # Allow anything up to VIDEO_ID,
          [^\w\s-]       # but char before ID is non-ID char.
        )                 # End host alternatives.
        ([\w-]{11})      # $1: VIDEO_ID is exactly 11 chars.
        (?=[^\w-]|$)     # Assert next char is non-ID or EOS.
        (?!               # Assert URL is not pre-linked.
          [?=&+%\w.-]*    # Allow URL (query) remainder.
          (?:             # Group pre-linked alternatives.
            [\'"][^<>]*>  # Either inside a start tag,
          | </a>          # or inside <a> element text contents.
          )               # End recognized pre-linked alts.
        )                 # End negative lookahead assertion.
        [?=&+%\w.-]*        # Consume any URL (query) remainder.
        """, re.VERBOSE)

    string = youtube_regex.sub('<div class="youtube-embed" data-youtube-id="\\1"></div>', string)


    soundcloud_regex = re.compile(r'https://soundcloud.com/.[^\s.,"\']+')
    if soundcloud_regex.match(string):
        soundcloud_client = client = soundcloud.Client(
            client_id=app.config['SOUNDCLOUD_CLIENT_ID'])
        string = soundcloud_regex.sub(replace_track, string)

        def replace_track(matchobj):
            track = soundcloud_client.get('/resolve', url=matchobj.group(0))
            return '<div class="soundcloud-embed" data-soundcloud-id="' + track.id + '"></div>'

    return string


