import db
from main import database as d

def upgrade(dry_run=True):
    threads = db.MessageThread.query.all()
    print "Total", len(threads)
    count = 1
    missing_threads = []
    for thread in threads:
        print "Started for thread", count, thread.id
        other_user = thread.get_other_user(thread.user_id)
        if not other_user:
            missing_threads.append(thread)
            continue
        other_user_id = other_user.id
        users = [other_user_id, thread.user_id]
        message_users = db.MessageThreadUser.query.filter_by(thread_id=thread.id).all()
        for mu in message_users:
            mu.latest_message_body = thread.latest_message_body
            mu.other_user_id = get_other_user(mu.user_id, users)
            mu.updated_at = mu.updated_at
            if not dry_run:
                d.session.commit()
        print "Done for thread", thread.id
        count += 1
    print "All Done", len(missing_threads)
    print "now delete the missing threads"
    for t in missing_threads:
        if not dry_run:
            d.session.delete(t)
            d.session.commit()


def get_other_user(user_id, users):
    others = [u for u in users if u != user_id]
    return others[0]
