from elasticsearch import Elasticsearch
from main import app
from search import tasks
import db


def update_all_users():
    es = Elasticsearch(['http://172.31.39.143'])
    users = db.User.query.filter(db.User.id > 0).all()
    for user in users:
        if user.profile and user.profile.role_id:
            doc = tasks._build_doc(user)
            try:
                res = es.index(
                    index='users',
                    doc_type=user.profile.role.slug,
                    id=user.id,
                    body={'doc': doc})
                print "Done for", user.id
            except Exception, e:
                print e, e.message

