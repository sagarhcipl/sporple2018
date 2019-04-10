#!/usr/bin/python
import os

if os.environ.get('ENVIRONMENT') == 'prod':
    os.environ['APP_CONFIG_FILE'] = '../config/prod.cfg'
elif os.environ.get('ENVIRONMENT') == 'staging':
    os.environ['APP_CONFIG_FILE'] = '../config/staging.cfg'
else:
    os.environ['APP_CONFIG_FILE'] = '../config/dev.cfg'

from main import app

application = app
app.secret_key = app.config['APP_SECRET']
if __name__ == '__main__':
    app.run(debug=True)
