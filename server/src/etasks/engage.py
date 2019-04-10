from main import app # order is important
import datetime
import db
from main import celery
from main import sentry
from etasks import emails
from sqlalchemy import func
from sqlalchemy import or_

# Daily
def engage_clubs():
    clubs = (db.UserProfile.query
        .filter_by(role_id=3)
        .order_by(func.random())
        .limit(300)
        .all())
    for club in clubs:
        send_recommendations_club.delay(club.user_id)


def engage_agents():
    agents = (db.UserProfile.query
        .filter_by(role_id=1)
        .order_by(func.random())
        .limit(300)
        .all())
    for agent in agents:
        send_recommendations_agent.delay(agent.user_id)


def engage_athletes():
    now = datetime.datetime.now()
    yday = now - datetime.timedelta(days=1)

    listings = (db.Listing.query
        .filter(db.Listing.created_at > yday)
        .filter_by(status='active')
        .limit(5)
        .all())

    if not listings:
        listings = (db.Listing.query
            .filter_by(status='active')
            .order_by(func.random())
            .limit(5)
            .all())

    listing_ids = [l.id for l in listings]

    athletes = (db.UserProfile.query
        .filter_by(role_id=2)
        .order_by(func.random())
        .limit(300)
        .all())
    for athlete in athletes:
        emails.send_opportunities_athlete.delay(athlete.user_id, listing_ids)


# Weekly
def engage_clubs_with_no_listing():
    clubs = (db.UserProfile.query
            .filter_by(role_id=3)
            .filter(~db.UserProfile.listings.any())
            .order_by(func.random())
            .limit(200)
            .all())
    for club in clubs:
        emails.send_no_listing.delay(club.id)

def engage_incomplete_profiles():
    athletes = (db.UserProfile.query
            .filter_by(role_id=2)
            .filter(or_(
                db.UserProfile.address_country_id != None,
                db.UserProfile.reel_video_url != None,
                db.UserProfile.height != None,
                db.UserProfile.weight != None,
                db.UserProfile.image != None))
            .order_by(func.random())
            .limit(200)
            .all())
    for athlete in athletes:
        emails.send_incomplete_athlete.delay(athlete.id)


def engage_agents_not_looking():
    agents = (db.UserProfile.query
            .filter_by(role_id=1)
            .filter(~db.UserProfile.looking_for_list.any())
            .order_by(func.random())
            .limit(200)
            .all())
    for agent in agents:
        emails.send_not_looking.delay(agent.id)


@celery.task()
def send_recommendations_club(club_id):
    # See if club has listings
    profiles = _get_completed_athlete_profiles()
    club = db.User.query.get(club_id)
    emails.send_recommendations_club(club, profiles)


@celery.task()
def send_recommendations_agent(agent_id):
    profiles = _get_completed_athlete_profiles()
    agent = db.User.query.get(agent_id)
    emails.send_recommendations_agent(agent, profiles)


def _get_completed_athlete_profiles():
    return (db.UserProfile.query
            .filter_by(role_id=2)
            .filter(db.UserProfile.address_country_id != None)
            .filter(db.UserProfile.reel_video_url != None)
            .filter(db.UserProfile.height != None)
            .filter(db.UserProfile.weight != None)
            .filter(db.UserProfile.image != None)
            .order_by(func.random())
            .limit(5)
            .all())
