import boto
import db
import uuid
from main import app
from main import database as d
from auth import controller
from uploads import upload
from profile import tasks

def upgrade(dry_run=True):
    clients = db.Client.query.filter(db.Client.image != '').limit(1).all()
    print "found", len(clients)
    for client in clients:
        save_client(client, dry_run)

def save_client(client, dry_run):
    username = uuid.uuid4().hex[:15]
    user = db.User(username=username, password=username, salt='')
    profile = db.UserProfile(user=user, device='client-migration')
    profile.role_id = 2
    d.session.add(user)
    d.session.add(profile)
    profile.firstname = client.firstname
    profile.lastname = client.lastname
    profile.current_club = client.club_name
    profile.managed_by_id = client.user_id
    profile.slug = controller.ensure_slug(client.firstname + ' ' + client.lastname)
    user.sports = [client.user.sport]

    if client.image:
        b = upload._get_bucket()
        new_key = "uploads/profile/" + client.image
        old_key = 'uploads/client/' + client.image
        profile.image = client.image
        print old_key
        print new_key
        if not dry_run:
            b.copy_key(new_key, app.config['S3_BUCKET'], old_key)
            b.set_acl('public-read', new_key)
    if not dry_run:
        controller._create_user_tables(user)
        d.session.commit()
        if client.image:
            tasks.profile_image_uploaded.delay(user.id)
    print profile.user_id, profile.slug, "Done"

