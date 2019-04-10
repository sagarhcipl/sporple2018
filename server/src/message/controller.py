import db
import re
from main import database as d
from main import app
from uploads import upload
from etasks import emails


def get_thread_users_for(user, search_filter, page=0):
    threads_query = (db.MessageThreadUser.query
            .filter_by(user_id=user.id))

    if search_filter:
        threads_query = (threads_query
            .join(db.Message, db.Message.thread_id == db.MessageThreadUser.thread_id)
            .filter(db.Message.body.like('%' + search_filter + '%')))

    threads_query = threads_query.order_by(db.MessageThreadUser.updated_at.desc())
    threads_query = threads_query.limit(20)
    if page:
        threads_query = threads_query.offset(page*20)
    threads = threads_query.all()
    return threads


def get_thread(thread_id):
    return db.MessageThread.query.get(thread_id)


def get_message_users_for_thread(thread_id, user):
    return (db.MessageThreadUser.query
            .filter_by(thread_id=thread_id)
            .filter(db.MessageThreadUser.user_id != user.id)
            .all())


def get_messages(thread_id):
    messages = (db.Message.query
            .filter_by(thread_id=thread_id)
            .order_by(db.Message.id.desc())
            .limit(500)
            .all())
    return reversed(messages)

def get_user(user_id):
    return db.User.query.get(user_id)

def messages_read(user, thread_id):
    thread_user = (db.MessageThreadUser.query
            .filter_by(thread_id=thread_id)
            .filter_by(user_id=user.id)
            .first())
    if thread_user:
        messages_read = thread_user.nb_unread_messages
        if messages_read:
            thread_user.nb_unread_messages = 0
            message_user = db.MessageUser.query.get(user.id)
            if not message_user:
                message_user = db.MessageUser(user_id=user.id)
                d.session.add(message_user)
            message_user.nb_unread_messages -= messages_read
            if message_user.nb_unread_messages < 0:
                message_user.nb_unread_messages = 0
            d.session.commit()


def save_message_thread(from_user, thread, body, attachment_path):
    if from_user.role_slug == 'agent' and _has_email_or_link(body):
        raise UserWarning("Cannot send emails or URLS in message.")
    thread_users = (db.MessageThreadUser.query
            .filter_by(thread_id=thread.id)
            .all())
    message = db.Message(
        thread=thread,
        user_id=from_user.id,
        body=body)
    if attachment_path:
        message.attachment=attachment_path
    d.session.add(message)

    _new_message_inserted(thread, thread_users, message)
    d.session.commit()
    target_user_id = None
    for thread_user in thread_users:
        if thread_user.user_id != from_user.id:
            target_user_id = thread_user.user_id
    emails.notify_new_message.apply_async(
            args=[target_user_id, from_user.id, message.id], countdown=10)


def save_message_user(from_user, target_user, body, attachment_path):
    if from_user.role_slug == 'agent' and _has_email_or_link(body):
        raise UserWarning("Cannot send emails or URLs in message.")
    thread, thread_users, created = _retrieve_or_create_thread(
            [from_user.id, target_user.id])
    message = db.Message(
        thread=thread,
        user_id=from_user.id,
        body=body)
    if attachment_path:
        message.attachment=attachment_path
    d.session.add(message)

    _new_message_inserted(thread, thread_users, message)
    d.session.commit()
    emails.notify_new_message.apply_async(
            args=[target_user.id, from_user.id, message.id], countdown=10)


def _retrieve_or_create_thread(user_ids):
    user_ids_sorted = sorted(user_ids)
    user_ids_string = ','.join([str(i) for i in user_ids_sorted])
    thread = (db.MessageThread.query
            .filter_by(nb_thread_users = len(user_ids_sorted))
            .filter_by(user_ids_string=user_ids_string)
            .first())

    created = False
    if not thread:
        # Assuming two users only.
        user_id = user_ids[0] # Sender
        other_user_id = user_ids[1] # Receiver
        thread = db.MessageThread(
            user_id=user_id,
            user_ids_string=user_ids_string,
            nb_thread_users=len(user_ids))
        d.session.add(thread)
        thread_users = []

        thread_user = db.MessageThreadUser(
                thread=thread, user_id=user_id, other_user_id=other_user_id)
        d.session.add(thread_user)
        thread_users.append(thread_user)

        thread_other_user = db.MessageThreadUser(
                thread=thread, user_id=other_user_id, other_user_id=user_id)
        d.session.add(thread_other_user)
        thread_users.append(thread_other_user)
        created = True
    else:
        thread_users = (db.MessageThreadUser.query
            .filter_by(thread_id=thread.id)
            .all())
    return thread, thread_users, created


def _new_message_inserted(thread, thread_users, message):
    thread.latest_message_user_id = message.user_id
    thread.latest_message_attachment = message.attachment
    thread.latest_message_body = message.body

    for thread_user in thread_users:
        thread_user.latest_message_body = message.body

        if thread_user.user_id != message.user_id:
            thread_user.nb_unread_messages = (thread_user.nb_unread_messages or 0) + 1
            user = db.MessageUser.query.get(thread_user.user_id)
            if not user:
                user = db.MessageUser(user_id=thread_user.user_id)
                d.session.add(user)
            user.nb_unread_messages = (user.nb_unread_messages or 0) + 1


hyperlink_regex = re.compile(r'(http|)(s|)(://|)((([-\w]+\.)+([^\s\/]+))([^\s]*)[^,.\s])')
email_regex = re.compile(r'[\w\.\+-]+@[\w\.-]+')
def _has_email_or_link(text):
    return bool(hyperlink_regex.search(text)) or \
        bool(email_regex.search(text))
