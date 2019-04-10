import db

def get_followers_count(user):
    return db.UserConnection.query.filter_by(other_user_id=user.id).count()


def get_following_count(user):
    return db.UserConnection.query.filter_by(user_id=user.id).count()
