import db

from main import app


def get_looking_for_by_agent(agent_id=0):
    return (db.LookingFor.query
        .filter_by(user_id = agent_id)
        .order_by(db.LookingFor.created_at.desc())
        .all())


def get_looking_for_by_sport(sport_id, page):
    looking_for_list = (db.LookingFor.query
        .join(db.UserProfile, db.LookingFor.user_id == db.UserProfile.user_id)
        .filter(db.UserProfile.image.isnot(None))
        .filter_by(sport_id=sport_id)
        .order_by(db.LookingFor.created_at.desc())
        .paginate(page=page, per_page=20, error_out=False)
        .items)

    return looking_for_list


def get_looking_for_by_sports(sports, page):
    sport_ids = [sport.id for sport in sports]
    looking_for_list = (db.LookingFor.query
        .join(db.UserProfile, db.LookingFor.user_id == db.UserProfile.user_id)
        .filter(db.UserProfile.image.isnot(None))
        .filter(db.LookingFor.sport_id.in_(sport_ids))
        .order_by(db.LookingFor.created_at.desc())
        .paginate(page=page, per_page=20, error_out=False)
        .items)
    return looking_for_list



