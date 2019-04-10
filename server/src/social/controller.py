import datetime
import db
import os.path
import string
from config import image_sizes
from main import database as d
from main import sentry
from uploads import upload
from etasks import emails


def get_followers(user_id, page=0):
    # Fetch followers
    followers = (db.UserConnection.query
        .filter_by(other_user_id=user_id)
        .order_by(db.UserConnection.created_at.desc())
        .limit(20)
        .offset(page*20))
    users = [f.user for f in followers]
    return users


def get_following(user_id, page=0):
    following = (db.UserConnection.query
        .filter_by(user_id=user_id)
        .order_by(db.UserConnection.created_at.desc())
        .limit(20)
        .offset(page*20))
    users = [f.other_user for f in following]
    return users


def add_follow(user_id, other_user_id, notify=True):
    if user_id != other_user_id:
        # Check if already exist:
        connection = (db.UserConnection.query
            .filter_by(user_id=user_id)
            .filter_by(other_user_id=other_user_id)
            .first())
        if not connection:
            connection = db.UserConnection(
                user_id=user_id,
                other_user_id=other_user_id)
            d.session.add(connection)
            d.session.commit()
            if notify:
                emails.notify_new_follower.delay(other_user_id, user_id)


def remove_follow(user_id, other_user_id):
    connection = (db.UserConnection.query
        .filter_by(user_id=user_id)
        .filter_by(other_user_id=other_user_id)
        .first())
    if connection:
        d.session.delete(connection)
        d.session.commit()


def publish_post(user, form):
    body = form.body.data
    if 'sportsbridge' in body.lower():
        sentry.sendMessage("[SportsBridge'] Post flagged", extra={'body': body})
        return

    post = db.Post(body=form.body.data, user=user)
    if user.is_super_admin:
        post.global_all_roles = True
        post.sports = user.sports_list
    d.session.add(post)
    # To get post.id
    d.session.commit()

    has_attachment = False
    for i in range(0, 10):
        file = getattr(form, 'filename_%d' % i, None)
        if file and file.data:
            post_upload_dir = 'ooipAttachments/Post/default'
            filename = upload.s3_upload(file.data,
                sub_dir='/' + post_upload_dir)
            # Also serially upload resized
            file_path = '/uploads/' + post_upload_dir + '/' + filename
            resize_path = image_sizes.get_resized(file_path, 'thumb')
            upload.s3_resize(file_path, resize_path, 'thumb')

            original_file = os.path.splitext(filename)
            attachment = db.Attachment(
                    attachable_id = post.id,
                    attachable_model = 'Post',
                    filename = original_file[0],
                    folder = post_upload_dir,
                    fileextension = original_file[1][1:],
                    attachment_namespace = 'default')
            d.session.add(attachment)
            has_attachment = True

    if has_attachment:
        d.session.commit()


def delete_post(user, post_id):
    post = db.Post.query.get(int(post_id))
    if not post:
        return
    if post.user_id != user.id:
        raise UserWarning("Invalid request" + str(post_id))

    attachments = post.get_attachments()
    for attachment in attachments:
        d.session.delete(attachment)
    d.session.delete(post)
    d.session.commit()


def save_comment(post_id, user, text):
    post = db.Post.query.get(post_id)
    comment = db.Comment(
            commentable_model='Post',
            commentable_id=post.id,
            text=text,
            author_id=user.id)
    d.session.add(comment)
    d.session.commit()
    emails.notify_comment.delay(post.user_id, post.id, comment.id, user.id)


def favourite_post(post_id, user):
    post = db.Post.query.get(post_id)
    if not post.has_favourited(user.id):
        favourite = db.FavouritePost(
                post_id=post.id,
                user_id=user.id)
        d.session.add(favourite)
        d.session.commit()
        emails.notify_post_like.delay(post.id, user.id)

def unfavourite_post(post_id, user):
    post = db.Post.query.get(post_id)
    favourite = (db.FavouritePost.query
            .filter_by(post_id=post.id)
            .filter_by(user_id=user.id)
            .first())
    if favourite:
        d.session.delete(favourite)
        d.session.commit()

def get_user(user_id):
    return db.User.query.get(user_id)


def get_visitors(user_id, page):
    one_month = datetime.datetime.utcnow() - datetime.timedelta(days=30)
    visits_query = db.UserVisit.query \
            .filter_by(user_id=user_id) \
            .filter(db.UserVisit.updated_at > one_month)
    total_results = visits_query.count()
    visits = visits_query.order_by(db.UserVisit.updated_at.desc()) \
            .offset(page*20).limit(20)

    visitors = [v.visitor for v in visits]
    return visitors, total_results
