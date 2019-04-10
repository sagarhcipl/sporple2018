import db
from sqlalchemy import and_
from sqlalchemy import or_

def get_all_posts_for_sports(user, sports, role, page=1):
    # Find all users this user is following
    post_user_connections = (db.UserConnection.query
            .filter_by(user_id=user.id)
            .all())
    post_user_ids = [c.other_user_id for c in post_user_connections] + [user.id]

    sport_ids = [s.id for s in sports]

    exclude_welcome = (db.Post.welcome_post == False)
    sport_queries = []
    for sport_id in sport_ids:
        sport_queries.append(db.Post.sports.any(id=sport_id))
    filter_sports = or_(*sport_queries)
    global_all_sports = (db.Post.global_all_sports == True)
    posts_query = (db.Post.query.filter(or_(
        and_(db.Post.user_id.in_(post_user_ids), exclude_welcome),
        and_(db.Post.global_all_roles == True, global_all_sports),
        and_(db.Post.global_all_roles == True, filter_sports, exclude_welcome),
        and_(db.Post.global_role_id == role.id, global_all_sports, exclude_welcome),
        and_(db.Post.global_role_id == role.id, filter_sports, exclude_welcome),
        and_(db.Post.user_id != None, filter_sports, db.Post.welcome_post == True)))
        .order_by(db.Post.created_at.desc())
        .limit(5)
        .offset((page-1)*5))
    results = posts_query.all()
    return results

