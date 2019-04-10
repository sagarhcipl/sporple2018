BASE_NAME = 'Sporple'
BASE_URL = 'https://www.sporple.com'
BASE_TITLE = 'Sporple | Your Global Sporting Network'
BASE_EMAIL = 'admin@sporple.com'
BASE_FROM_NAME = 'Sporple Team'

APP_SECRET = 'SzfDW345zf/gvSF,$fdg 12'

SQLALCHEMY_TRACK_MODIFICATIONS = False
MAX_NR_ATTACHMENTS = 10
SENTRY_DSN = ''
SENTRY_PUBLIC_DSN = 'https://b0c08c190ade459ca810641b65dbd73c@app.getsentry.com/73263'
SESSION_TYPE = 'redis'

FACEBOOK_APP_PERMISSIONS = ['email', 'user_birthday', 'user_location']
FACEBOOK_OAUTH_URL = 'https://www.facebook.com/v2.8/dialog/oauth?client_id=%s&redirect_uri=%s&scope=%s'
FACEBOOK_USER_URL = 'https://graph.facebook.com/v2.8/oauth/access_token?client_id=%s&client_secret=%s&redirect_uri=%s&code=%s'
FACEBOOK_REQUEST_INFO_URL = 'https://graph.facebook.com/me/?access_token=%s'
TWITTER_WIDGET_ID = '443684845898563584'
TWITTER_CONSUMER_KEY = 'ythYWt5RXMk6VaezVg7w'
TWITTER_CONSUMER_SECRET = '7EwkRlrlbWiAqXKjbaMFQNrWktCA3aaOLkf2tQhwaaE'
TWITTER_ACCESS_TOKEN = '20018351-0TuxOaocoOf8Oq6TwrkDNtANmSLT8AvDpvOXcr38p'
TWITTER_ACCESS_TOKEN_SECRET = 'rjwqvoMBEtZbyuDOpq03WKDShsrmpEFc2evKOeSEHqLhK'
S3_BUCKET = 'sporple-uploads'
S3_UPLOAD_DIRECTORY = 'uploads'
S3_KEY = 'AKIAIBSLPUUAIIATE7VQ'
S3_SECRET = '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'
S3_UPLOAD_ENABLE = True

CELERY_IMPORTS= ('tasks')
BCC_EMAIL = 'sporple.bcc@gmail.com'
ELASTICSEARCH_HOST = '52.51.102.20:9200'
ADMIN_EMAILS = [
        {'email': 'ankit@sporple.com', 'name': 'Ankit Jain', 'type': 'to'},
        {'email': 'admin+web@sporple.com', 'name': 'Sporple Admin', 'type': 'to'},
        {'email': 'mat@sporple.com', 'name': 'Mat Cole', 'type': 'to'},
]

MAILCHIMP_API_KEY = 'b663ce7598faf842c88e887ecce0bc48-us7'
MAILCHIMP_SYNC_ENABLED = False

