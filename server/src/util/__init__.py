import binascii
import hashlib
import os
import re
import requests
import shutil
from datetime import datetime
from unicodedata import normalize


def generate_signature(hashed_code):
    return hashlib.sha1(hashed_code).hexdigest()


def _encrypt_password_with_salt(password, salt):
    return hashlib.sha1(salt + password).hexdigest()


def _encrypt_password_and_get_salt(password):
    salt = binascii.b2a_hex(os.urandom(16))
    password = _encrypt_password_with_salt(password, salt)
    return salt, password


def encrypt_password(password, salt=None):
    if not salt:
        return _encrypt_password_and_get_salt(password)
    else:
        return _encrypt_password_with_salt(password, salt)


def download_file(url, file_path):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_path, 'wb') as f:
            r.raw_decode_content = True
            shutil.copyfileobj(r.raw, f)
            return True
    return False


def is_valid_email(email):
    email = email.lower()
    _email_re = re.compile(r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}')
    match = _email_re.match(email)
    return bool(match)
   


def request_to_dict(args):
    all_list = args.lists()
    params = {}
    for val in all_list:
        params[val[0]] = val[1][0] if len(val[1]) == 1 else val[1]
    return params


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    return str(day_diff / 365) + " years ago"



def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))


def vimeo_id_from_url(url):
    _vimeo_re = re.compile('.*vimeo\.com\/([a-z]*\/)*([0-9]{6,11})[?]?.*')
    match = _vimeo_re.match(url)
    if match:
        return match.group(2)
    return None


def youtube_id_from_url(url):
    _youtube_re = re.compile(
            '(?:http|https|)' #Optional scheme. Either http or https
            + '(?::\/\/|)' #Optional scheme. ://
            + '(?:www.|)' #Optional scheme. www.
            + '(?:' #Group host alternatives
            + 'youtu\.be\/' #Either youtu.be
            + '|youtube\.com' #youtube.com
            + '(?:' #Group path alternatives.
            + '\/embed\/' #/embed
            + '|\/v\/' #or /v
            + '|\/watch\?v=' #/watch?v=
            + '|\/ytscreeningroom\?v=' #/ytscreeningroom?v=
            + '|\/feeds\/api\/videos\/' #or either /feeds or /api or /videos
            + '|\/user' #or /user
            + '\S*' #Allow anything upto "youtube VIDEO_ID" (Note: 1a)
            + '[^\w\-\s]' #but char before "youtube VIDEO_ID" is non-id char (Note: 2a)
            + '|\S*' #or Allow anything upto "youtube VIDEO_ID" (Note: 1b)
            + '[^\w\-\s]' #but char before "youtube VIDEO_ID" is non-id char (Note: 2b)
            + ')' #End group path alternatives
            + ')' #End host alternatives
            + '([\w\-]{11})' #"youtube VIDEO_ID" is exactly 11 chars
            + '[a-z0-9;:@?&%=+\/\$_.-]*',
            flags=re.IGNORECASE)

    match = _youtube_re.match(url)
    if match:
        return match.group(1)

    return 'blah'
