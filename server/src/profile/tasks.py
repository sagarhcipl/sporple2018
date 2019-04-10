import db
from etasks import mailchimp_sync
from main import celery
from main import database as d
from search import tasks as stask
from uploads import upload

@celery.task()
def user_profile_updated(id):
    stask.on_update(id)


@celery.task()
def user_registered(id):
    user = db.User.query.get(id)
    body = 'Has just signed up to Sporple, why don\'t you check out their profile!'
    welcome_post = db.Post(body=body, user_id=id,
            global_all_roles=True, welcome_post=True)
    welcome_post.sports = user.sports_list
    d.session.add(welcome_post)
    d.session.commit()
    stask.on_register(id)
    mailchimp_sync.subscribe_user.delay(id)

@celery.task()
def profile_image_uploaded(id):
    user = db.User.query.get(id)
    image_path = user.profile.get_image()
    sizes = ['large', 'small', 'x-small']
    for size in sizes:
        upload.s3_resize(image_path, user.profile.get_image(size), size, user_id_str=str(id))
    stask.on_update(id)

