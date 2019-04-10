import db
from main import database as d


def update(dry_run=True):
    preferences = db.UserEmailPreference.query.all()
    for pref in preferences:
        pref.recommendations = True
        pref.reminders = True
    if not dry_run:
        d.session.commit()

