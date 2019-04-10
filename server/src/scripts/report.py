from main import app # order is important
import datetime
import db
from etasks import emails
from main import database as d


def generate_daily_report():
    now = datetime.datetime.now()
    yday = now - datetime.timedelta(days=1)
    params = _get_params_since(yday, now)
    params['duration'] = now.strftime('%b %d, %Y')
    emails.send_daily_report.delay(params)

    # Update database
    stats = (db.DailyStats(
        listings=params.get('new_listings', 0),
        applications=params.get('new_apps', 0),
        users=params.get('total_new_users', 0),
        clubs=params.get('new_clubs', 0),
        agents=params.get('new_agents', 0),
        athletes=params.get('new_athletes', 0),
        unknown_users=params.get('new_unknown_users', 0),
        messages=params.get('new_messages', 0),
        club_messages=params.get('new_club_msgs', 0),
        agent_messages=params.get('new_agent_msgs', 0),
        athlete_messages=params.get('new_athlete_msgs', 0),
        threads=params.get('new_threads', 0),
        club_threads=params.get('new_club_threads', 0),
        agent_threads=params.get('new_agent_threads', 0),
        athlete_threads=params.get('new_athlete_threads', 0),
        connections=params.get('new_connections', 0),
        looking_for=params.get('new_looking_for', 0),
        posts=params.get('new_posts', 0)
        ))
    d.session.add(stats)
    d.session.commit()


def generate_weekly_report():
    now = datetime.datetime.now()
    last_week = now - datetime.timedelta(days=7)
    params = _get_params_since(last_week, now)
    params['duration'] = last_week.strftime('%b %d, %Y') \
            + ' to ' + now.strftime('%b %d, %Y')
    emails.send_weekly_report.delay(params)

    # Update database
    stats = (db.WeeklyStats(
        start=last_week,
        end=now,
        listings=params.get('new_listings', 0),
        applications=params.get('new_apps', 0),
        users=params.get('total_new_users', 0),
        clubs=params.get('new_clubs', 0),
        agents=params.get('new_agents', 0),
        athletes=params.get('new_athletes', 0),
        unknown_users=params.get('new_unknown_users', 0),
        messages=params.get('new_messages', 0),
        club_messages=params.get('new_club_msgs', 0),
        agent_messages=params.get('new_agent_msgs', 0),
        athlete_messages=params.get('new_athlete_msgs', 0),
        threads=params.get('new_threads', 0),
        club_threads=params.get('new_club_threads', 0),
        agent_threads=params.get('new_agent_threads', 0),
        athlete_threads=params.get('new_athlete_threads', 0),
        connections=params.get('new_connections', 0),
        looking_for=params.get('new_looking_for', 0),
        posts=params.get('new_posts', 0)
        ))
    d.session.add(stats)
    d.session.commit()


def _get_params_since(time, end_time=None):
    params = {}
    # Find new applications since time
    apps_params = _new_applications_since(time, end_time)
    params.update(apps_params)

    # Find new listings since time
    list_params = _new_listings_since(time, end_time)
    params.update(list_params)

    # Find new users since time
    user_params = _new_users_since(time, end_time)
    params.update(user_params)

    # Find new messages since time
    message_params = _new_messages_since(time, end_time)
    params.update(message_params)

    # Find new connections since time
    conn_params = _new_conns_since(time, end_time)
    params.update(conn_params)

    # Find new looking for since time
    lf_params = _new_looking_for_since(time, end_time)
    params.update(lf_params)

    # Find new posts since time
    post_params = _new_posts_since(time, end_time)
    params.update(post_params)

    print params
    return params


def _new_applications_since(time, end_time):
    applications = (db.Application.query
        .filter(db.Application.created_at > time)
        .filter(db.Application.created_at < end_time)
        .order_by(db.Application.listing_id.desc())
        .all())
    params = {}
    params['new_apps'] = len(applications)
    params['apps'] = []

    app_count = 0
    listing_id = 0
    for app in applications:
        if listing_id != app.listing_id:
            listing = app.listing
            listing_info = {
                'club_name': listing.club.name,
                'position': listing.position.name,
                'count': 1,
            }
            params['apps'].append(listing_info)
            listing_id = app.listing_id
        else:
            listing_info['count'] += 1

    return params


def _new_listings_since(time, end_time):
    listings = (db.Listing.query
        .filter(db.Listing.created_at > time)
        .filter(db.Listing.created_at < end_time)
        .filter(db.Listing.status == 'active')
        .order_by(db.Listing.club_id.desc())
        .all())
    params = {}
    params['new_listings'] = len(listings)
    params['listings'] = []
    for listing in listings:
        params['listings'].append({
            'club_name': listing.club.name,
            'position': listing.position.name
        })

    return params


def _new_users_since(time, end_time):
    users = (db.User.query
        .filter(db.User.created_at > time)
        .filter(db.User.created_at < end_time)
        .all())
    params = {}
    params['total_new_users'] = len(users)

    athletes = 0
    clubs = 0
    agents = 0
    unknown = 0
    for user in users:
        role_slug = user.role_slug
        if role_slug == 'athlete':
            athletes += 1
        elif role_slug == 'club':
            clubs += 1
        elif role_slug == 'agent':
            agents += 1
        else:
            unknown += 1
    params['new_clubs'] = clubs
    params['new_agents'] = agents
    params['new_athletes'] = athletes
    params['new_unknown_users'] = unknown

    return params


def _new_conns_since(time, end_time):
    conns = (db.UserConnection.query
        .filter(db.UserConnection.created_at > time)
        .filter(db.UserConnection.created_at < end_time)
        .all())
    params = {}
    params['new_connections'] = len(conns)
    return params


def _new_messages_since(time, end_time):
    messages = (db.Message.query
        .filter(db.Message.created_at > time)
        .filter(db.Message.created_at < end_time)
        .all())
    params = {}
    params['new_messages'] = len(messages)

    athletes = 0
    clubs = 0
    agents = 0
    for message in messages:
        role_slug = message.user.role_slug
        if role_slug == 'athlete':
            athletes += 1
        if role_slug == 'club':
            clubs += 1
        if role_slug == 'agent':
            agents += 1
    params['new_athlete_msgs'] = athletes
    params['new_club_msgs'] = clubs
    params['new_agent_msgs'] = agents

    threads = (db.MessageThread.query
        .filter(db.MessageThread.created_at > time)
        .filter(db.MessageThread.created_at < end_time)
        .all())

    params['new_threads'] = len(threads)
    athletes = 0
    clubs = 0
    agents = 0
    for thread in threads:
        role_slug = thread.user.role_slug
        if role_slug == 'athlete':
            athletes += 1
        if role_slug == 'club':
            clubs += 1
        if role_slug == 'agent':
            agents += 1
    params['new_athlete_threads'] = athletes
    params['new_club_threads'] = clubs
    params['new_agent_threads'] = agents
    return params


def _new_looking_for_since(time, end_time):
    looking_for_list = (db.LookingFor.query
        .filter(db.LookingFor.created_at > time)
        .filter(db.LookingFor.created_at > end_time)
        .all())
    params = {}
    params['new_looking_for'] = len(looking_for_list)
    return params

def _new_posts_since(time, end_time):
    posts = (db.Post.query
        .filter(db.Post.created_at > time)
        .filter(db.Post.created_at < end_time)
        .all())
    params = {}
    params['new_posts'] = len(posts)
    return params

def prepopulate_daily_report():
    now = datetime.datetime.now()
    yday = now - datetime.timedelta(days=1)

    begin = datetime.datetime(2016, 1, 1)
    end = now
    while begin < end:
        start = begin
        finish = start + datetime.timedelta(days=1)
        params = _get_params_since(start, finish)

        # Update database
        stats = (db.DailyStats(
            created_at=finish,
            listings=params.get('new_listings', 0),
            applications=params.get('new_apps', 0),
            users=params.get('new_users', 0),
            clubs=params.get('new_clubs', 0),
            agents=params.get('new_agents', 0),
            athletes=params.get('new_athletes', 0),
            unknown_users=params.get('new_unknown_users', 0),
            messages=params.get('new_messages', 0),
            club_messages=params.get('new_club_msgs', 0),
            agent_messages=params.get('new_agent_msgs', 0),
            athlete_messages=params.get('new_athlete_msgs', 0),
            threads=params.get('new_threads', 0),
            club_threads=params.get('new_club_threads', 0),
            agent_threads=params.get('new_agent_threads', 0),
            athlete_threads=params.get('new_athlete_threads', 0),
            connections=params.get('new_connections', 0),
            looking_for=params.get('new_looking_for', 0),
            posts=params.get('new_posts', 0)
            ))
        d.session.add(stats)
        d.session.commit()
        begin = finish
        print "Done for ", finish


def prepopulate_weekly_report():
    begin = datetime.datetime(2016, 1, 1)
    end = datetime.datetime(2016, 5, 2, hour=14)
    # start with end so we can keep weeks consistent
    while begin < end:
        finish = end
        start = end - datetime.timedelta(days=7)
        params = _get_params_since(start, finish)

        # Update database
        stats = (db.WeeklyStats(
            created_at=finish,
            start=start,
            end=finish,
            listings=params.get('new_listings', 0),
            applications=params.get('new_apps', 0),
            users=params.get('new_users', 0),
            clubs=params.get('new_clubs', 0),
            agents=params.get('new_agents', 0),
            athletes=params.get('new_athletes', 0),
            unknown_users=params.get('new_unknown_users', 0),
            messages=params.get('new_messages', 0),
            club_messages=params.get('new_club_msgs', 0),
            agent_messages=params.get('new_agent_msgs', 0),
            athlete_messages=params.get('new_athlete_msgs', 0),
            threads=params.get('new_threads', 0),
            club_threads=params.get('new_club_threads', 0),
            agent_threads=params.get('new_agent_threads', 0),
            athlete_threads=params.get('new_athlete_threads', 0),
            connections=params.get('new_connections', 0),
            looking_for=params.get('new_looking_for', 0),
            posts=params.get('new_posts', 0)
            ))
        d.session.add(stats)
        d.session.commit()
        end = start
        print "Done for ", finish

