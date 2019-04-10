import db
from main import database as d
from etasks import emails


'''
For clubs
'''
def get_current_team(club_profile):
    return (db.Relate.query
        .filter_by(user_id=club_profile.user_id)
        .filter_by(type='current_player')
        .order_by(db.Relate.year_start.desc())
        .all())



def get_past_team(club_profile):
    return (db.Relate.query
        .filter_by(user_id=club_profile.user_id)
        .filter_by(type='past_player')
        .order_by(db.Relate.year_start.desc())
        .all())


def get_legends(profile):
    return (db.Relate.query
        .filter_by(user_id=profile.user_id)
        .filter_by(is_legend=True)
        .order_by(db.Relate.year_start.desc())
        .all())


'''
For athletes
'''
def get_played_with(athlete_profile):
    return (db.Relate.query
        .filter_by(user=athlete_profile.user_id)
        .filter_by(type='played_with')
        .order_by(db.Relate.year_start.desc())
        .all())


'''
For agents
'''
def get_current_clients(profile):
    return (db.Relate.query
        .filter_by(user_id=profile.user_id)
        .filter_by(type='current_client')
        .order_by(db.Relate.year_start.desc())
        .all())


def get_past_clients(profile):
    return (db.Relate.query
        .filter_by(user_id=profile.user_id)
        .filter_by(type='past_clients')
        .order_by(db.Relate.year_start.desc())
        .all())


'''
Generic setters
'''
def set_relation(user, target_user,
        year_start, year_end, club_name='',
        type='current_player'):
    target_role_slug = target_user.role_slug
    user_role_slug = user.role_slug
    athlete = None
    club = None
    primary_user = user

    if target_role_slug == 'athlete':
        athlete = target_user
    elif user_role_slug == 'athlete':
        athlete = user
        primary_user = target_user
    elif target_role_slug == 'club':
        # none is athlete, set club
        club = target_user
    elif user_role_slug == 'club':
        club = user
        primary_user = target_user

    # Check if the athlete is already related
    if athlete:
        relation = (db.Relate.query
            .filter_by(user_id=primary_user.id)
            .filter_by(athlete_id=athlete.id)
            .first())
        if not relation:
            relation = db.Relate(
                user_id=primary_user.id,
                athlete_id=athlete.id,
                created_by=user_role_slug,
                user_role=primary_user.role_slug)
            d.session.add(relation)
    elif club:
        relation = (db.Relate.query
            .filter_by(user_id=primary_user.id)
            .filter_by(club_id=club.id)
            .first())
        if not relation:
            relation = db.Relate(
                user_id=primary_user.id,
                club_id=club.id,
                created_by=user_role_slug,
                user_role=primary_user.role_slug)
            d.session.add(relation)
    else:
        # Ignore agent and agent interactions
        return

    relation.type = type
    if year_start:
        relation.year_start = int(year_start)
    if year_end:
        relation.year_end = int(year_end)

    emails.notify_new_relation.delay(type, target_user.id, user.id)
    d.session.commit()


def delete_relation(user_id, target_id):
    relation = (db.Relate.query
            .filter_by(user_id=user_id)
            .filter_by(athlete_id=target_id)
            .first())
    if not relation:
        relation = (db.Relate.query
            .filter_by(user_id=target_id)
            .filter_by(athlete_id=user_id)
            .first())
    if relation:
        d.session.delete(relation)
        d.session.commit()


def set_legend(profile, athlete_user_id):
    relations = (db.Relate.query
        .filter_by(user_id=profile.user_id)
        .filter_by(athlete_id=athlete_user_id)
        .all())

    if not relations:
        raise UserWarning("Could not find relation")
    relations[0].is_legend = True
    d.session.commit()


def unset_legend(profile, athlete_user_id):
    relations = (db.Relate.query
        .filter_by(user_id=profile.user_id)
        .filter_by(athlete_id=athlete_user_id)
        .all())

    if not relations:
        raise UserWarning("Could not find relation")
    relations[0].is_legend = False
    d.session.commit()


