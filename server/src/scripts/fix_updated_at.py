import db
from main import database as d

def fix(dry_run=True):
  threads = db.MessageThread.query.all()
  print "Total", len(threads)
  count = 1
  for thread in threads:
    print "Started for thread", count, thread.id
    message_users = db.MessageThreadUser.query.filter_by(thread_id=thread.id).all()
    count += 1
    for mu in message_users:
      mu.updated_at = thread.updated_at

  if not dry_run:
    d.session.commit()
  print "All done"
