from __future__ import absolute_import
import datetime
import db
import mimetypes
import os.path
import random
import util
from config import image_sizes
from main import app
from main import database as d
from auth import controller as auth_controller
from uploads import upload
from profile import tasks
from sqlalchemy import func
from flask.ext.login import current_user
from listing import controller as lcontroller

from sqlalchemy import or_
from werkzeug.utils import secure_filename


def get_total_users():
    return d.session.query(func.count(db.User.id)).scalar()


def get_featured_profiles(limit=4, athletes_only=True):
    profiles = db.UserProfile.query.filter(
        db.UserProfile.user_id.in_(app.config['FEATURED_USER_ID_LIST'])).all()
    if athletes_only:
        profiles = [p for p in profiles if p.role.slug == 'athlete']
    return random.sample(profiles, limit)


def get_profile_from_user_id(user_id):
    profile = db.UserProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        raise UserWarning("Invalid profile")
    return profile


def get_profile_from_slug(slug):
    from main import sentry

    profile = db.UserProfile.query.filter_by(slug=slug).first()
    if not profile:
        # Hack to resolve slug with number in end.
        i = slug.rfind('-')
        if i != -1 and slug[i + 1:].isdigit():
            slug = slug[:i]
            profile = db.UserProfile.query.filter_by(slug=slug).first()
            sentry.captureMessage('Invalid profile slug', extra={'slug': slug})

    if not profile:
        raise UserWarning("Invalid profile")
    return profile, slug


def get_posts_for_user(user_id):
    posts = (db.Post.query
             .filter_by(user_id=user_id)
             .filter_by(welcome_post=False)
             .order_by(db.Post.created_at.desc())
             .limit(5)
             .all())
    return posts


def get_team(profile):
    relations = (db.Relate.query
                 .filter_by(user_id=profile.user_id)
                 .filter(db.Relate.type.in_(('played_with', 'current_play_with')))
                 .order_by(db.Relate.created_at.desc())
                 .limit(10)
                 .all())

    users = [relate.athlete for relate in relations]
    return users


def get_current_team(profile):
    relations = (db.Relate.query
                 .filter_by(user_id=profile.user_id)
                 .filter_by(type='current_team')
                 .order_by(db.Relate.created_at.desc())
                 .limit(10)
                 .all())

    return [relate.athlete for relate in relations]


def get_past_team(profile):
    relations = (db.Relate.query
                 .filter_by(user_id=profile.user_id)
                 .filter_by(type='past_team')
                 .order_by(db.Relate.created_at.desc())
                 .limit(10)
                 .all())
    return [relate.athlete for relate in relations]


def update_athlete_profile(profile, form):
    slug = profile.slug
    if profile.firstname != form.firstname.data or profile.lastname != form.lastname.data:
        name = form.firstname.data + ' ' + form.lastname.data
        slug = ensure_slug(name)
        # Save user position list
    form.update_profile(profile)
    profile.slug = slug
    d.session.commit()

    tasks.user_profile_updated.delay(profile.user_id)


def save_player_media(profile, form):
    if form.reel_image.data:
        x1 = int(form.reel_image_x1.data)
        y1 = int(form.reel_image_y1.data)
        w = int(form.reel_image_w.data)
        h = int(form.reel_image_h.data)
        reel_image = upload.s3_resize_and_upload(
            form.reel_image.data,
            x1=x1, y1=y1, w=w, h=h,
            w_size=640, h_size=360,
            sub_dir='/profile/reel')
        profile.reel_video_url = ''
        profile.reel_video_url_original = ''

        filename = os.path.splitext(reel_image)
        extension = filename[1]
        profile.reel_image = ('/'
                              + app.config["S3_UPLOAD_DIRECTORY"]
                              + '/profile/reel/'
                              + reel_image)
    elif form.reel_video_url.data:
        video_url = form.reel_video_url.data
        video_id = ''
        if 'vimeo' in video_url:
            video_id = util.vimeo_id_from_url(video_url)
            profile.reel_video_type = 'vimeo'
        else:
            video_id = util.youtube_id_from_url(video_url)
            profile.reel_video_type = 'youtube'
        if not video_id:
            profile.reel_video_type = ''
            profile.reel_video_url_original = ''
            raise UserWarning("Invalid video url")
        else:
            profile.reel_video_url_original = video_url
            profile.reel_video_url = video_id
            profile.reel_image = ''

    d.session.commit()


def upload_photo(profile, form):
    if form.profile_image.data:
        if form.profile_image_x1.data and form.profile_image_y1.data:
            x1 = int(form.profile_image_x1.data)
            y1 = int(form.profile_image_y1.data)
            w = int(form.profile_image_w.data)
            h = int(form.profile_image_h.data)
            rotation = int(form.profile_rotation.data)
            profile.image = upload.s3_resize_and_upload(
                form.profile_image.data,
                x1=x1, y1=y1, w=w, h=h, rotation=rotation,
                sub_dir='/profile')
        else:
            profile.image = upload.s3_upload(
                form.profile_image.data, sub_dir='/profile')

        d.session.commit()
        tasks.profile_image_uploaded.delay(profile.user_id)


def _upload_agency_image(profile, form):
    if form.profile_agency_image.data:
        if form.profile_agency_image_x1.data and form.profile_agency_image_y1.data:
            x1 = int(form.profile_agency_image_x1.data)
            y1 = int(form.profile_agency_image_y1.data)
            w = int(form.profile_agency_image_w.data)
            h = int(form.profile_agency_image_h.data)
            rotation = int(form.profile_agency_rotation.data)
            profile.agency_image = upload.s3_resize_and_upload(
                form.profile_agency_image.data,
                x1=x1, y1=y1, w=w, h=h, rotation=rotation,
                sub_dir='/profile')
        else:
            profile.agency_image = upload.s3_upload(
                form.profile_agency_image.data,
                sub_dir='/profile')
        # Generate the thumb version
        file_path = '/uploads/profile/' + profile.agency_image
        resize_path = image_sizes.get_resized(file_path, 'small')
        upload.s3_resize(file_path, resize_path, 'small')


def update_agent_profile(profile, form):
    slug = profile.slug
    if profile.firstname != form.firstname.data or profile.lastname != form.lastname.data:
        name = form.firstname.data + ' ' + form.lastname.data
        slug = ensure_slug(name)
    _upload_agency_image(profile, form)

    form.update_profile(profile)
    profile.slug = slug
    d.session.commit()

    tasks.user_profile_updated.delay(profile.user_id)


def update_club_profile(profile, form):
    slug = profile.slug
    if profile.club_name != form.club_name.data:
        slug = ensure_slug(form.club_name.data)

    form.populate_obj(profile)
    profile.slug = slug
    d.session.commit()

    tasks.user_profile_updated.delay(profile.user_id)


def update_user_visit(user_id, visitor_id):
    if user_id == visitor_id:
        return
    visit = db.UserVisit.query \
        .filter_by(user_id=user_id) \
        .filter_by(visitor_id=visitor_id) \
        .first()
    if visit:
        visit.updated_at = datetime.datetime.utcnow()
    else:
        visit = db.UserVisit(user_id=user_id, visitor_id=visitor_id)
        d.session.add(visit)
    d.session.commit()


'''
Career Item - fetch, add, edit and delete.
'''


def get_career_item(id):
    career_item = db.CareerItem.query.get(id)
    if not career_item:
        raise UserWarning("Invalid career_item" + str(id))
    return career_item


def delete_career_item(user, career_item):
    if user and user.id == career_item.user.id:
        d.session.delete(career_item)
        d.session.commit()
    else:
        raise UserWarning("Invalid action, cannot delete career item")


def save_career_item(form, career_item, profile):
    if career_item and profile.user_id != career_item.user_id:
        raise UserWarning("Invalid action, cannot update career item")

    if not career_item:
        career_item = db.CareerItem(
            user_id=profile.user_id)
        d.session.add(career_item)
    form.update_obj(career_item)
    if form.item_image.data:
        sub_dir = '/careerItem'
        filename = upload.s3_upload(form.item_image.data, sub_dir=sub_dir)
        file_path = '/uploads' + sub_dir + '/' + filename
        career_item.image = filename
        career_item.original_image_name = form.item_image.data.filename
        resize_path = image_sizes.get_resized(file_path, 'icon')
        upload.s3_resize(file_path, resize_path, 'icon')

    d.session.commit()


def get_career_items(profile):
    return (db.CareerItem.query
            .filter_by(user_id=profile.user.id)
            .order_by(db.CareerItem.date_from.desc())
            .all())


'''
Agent's qualifications - fetch, add, edit and delete
'''


def get_qualification(id):
    qualification = db.Qualification.query.get(id)
    if not qualification:
        raise UserWarning("Invalid qualification" + str(id))
    return qualification


def delete_qualification(user, qualification):
    if user and user.id == qualification.user_id:
        d.session.delete(qualification)
        d.session.commit()
    else:
        raise UserWarning("Invalid action, cannot delete qualification")


def save_qualification(form, qualification, profile):
    if qualification and profile.user_id != qualification.user_id:
        raise UserWarning("Invalid action, cannot update qualification")

    if not qualification:
        qualification = db.Qualification(
            user_id=profile.user_id)
        d.session.add(qualification)
    form.populate_obj(qualification)
    d.session.commit()


def get_qualifications(profile):
    return (db.Qualification.query
            .filter_by(user_id=profile.user_id)
            .order_by(db.Qualification.year.desc())
            .all())


'''
Agent's clients - fetch, add, edit and delete.
'''


def get_client(id):
    client = db.Client.query.get(id)
    if not client:
        raise UserWarning("Invalid client" + str(id))
    return client


def get_clients(profile):
    users = db.UserProfile.query.filter_by(managed_by_id=profile.user_id).all()

    # And get relations too
    relations = (db.Relate.query
                 .filter_by(user_id=profile.user_id)
                 .filter_by(type='current_client')
                 .order_by(db.Relate.created_at.desc())
                 .limit(8)
                 .all())
    related_users = [relate.athlete.profile for relate in relations]
    for r in related_users:
        r.relate = True
    return users + related_users


def get_past_clients(profile):
    # And get relations too
    relations = (db.Relate.query
                 .filter_by(user_id=profile.user_id)
                 .filter(db.Relate.type.in_(('past_client')))
                 .order_by(db.Relate.created_at.desc())
                 .limit(10)
                 .all())
    related_users = [relate.athlete.profile for relate in relations]
    return related_users


def delete_client(user, client):
    if user and user.id == client.user_id:
        d.session.delete(client)
        d.session.commit()
    else:
        raise UserWarning("Invalid action, cannot delete client")


'''
Achievements - fetch, add, edit and delete.
'''


def get_achievement(id):
    achievement = db.Achievement.query.get(id)
    if not achievement:
        raise UserWarning("Invalid achievement" + str(id))
    return achievement


def delete_achievement(user, achievement):
    if user and user.id == achievement.user.id:
        d.session.delete(achievement)
        d.session.commit()
    else:
        raise UserWarning("Invalid action, cannot delete achievement")


def save_achievement(form, achievement, profile):
    if achievement and profile.user_id != achievement.user_id:
        raise UserWarning("Invalid action, cannot update achievement")

    if not achievement:
        achievement = db.Achievement(user_id=profile.user_id)
        d.session.add(achievement)
    form.populate_obj(achievement)
    d.session.commit()


def get_achievements_chronologically(profile):
    return (db.Achievement.query
            .filter_by(user_id=profile.user.id)
            .order_by(db.Achievement.year.desc())
            .all())


'''
Endorsements - fetch, add, edit and delete.
'''


def get_endorsement(id):
    endorsement = db.Endorsement.query.get(id)
    if not endorsement:
        raise UserWarning("Invalid endorsement" + str(id))
    return endorsement


def delete_endorsement(user, endorsement):
    if user and user.id == endorsement.user.id:
        d.session.delete(endorsement)
        d.session.commit()
    else:
        raise UserWarning("Invalid action, cannot delete endorsement")


def save_endorsement(form, endorsement, profile):
    if endorsement and profile.user_id != endorsement.user_id:
        raise UserWarning("Invalid action, cannot update endorsement")

    if not endorsement:
        endorsement = db.Endorsement(
            user_id=profile.user_id)
        d.session.add(endorsement)
    form.update_obj(endorsement)
    d.session.commit()


def get_endorsements(profile):
    return db.Endorsement.query.filter_by(user_id=profile.user.id).all()


'''
Looking For - fetch, add, edit and delete.
'''


def get_looking_for(id):
    looking_for = db.LookingFor.query.get(id)
    if not looking_for:
        raise UserWarning("Invalid looking_for: " + str(id))
    return looking_for


def delete_looking_for(user, looking_for):
    if user and user.id == looking_for.user_id:
        d.session.delete(looking_for)
        d.session.commit()
    else:
        raise UserWarning("Invalid action, cannot delete looking for")


def save_looking_for(form, looking_for, profile):
    if looking_for and profile.user_id != looking_for.user_id:
        raise UserWarning("Invalid action, cannot update looking for")

    if not looking_for:
        looking_for = db.LookingFor(user_id=profile.user_id)
        d.session.add(looking_for)
    form.update_obj(looking_for, profile.user.is_premium())
    d.session.commit()


def get_looking_for_list(profile):
    return db.LookingFor.query.filter_by(user_id=profile.user_id).all()


'''
Listings - fetch, add, edit and delete.
'''


def get_listing(id):
    listing = db.Listing.query.filter_by(id=id).first()
    if not listing:
        raise UserWarning("Invalid listing: " + str(id))
    return listing


def delete_listing(user, listing, closed_reason, hired_user_id,
                   athlete_name, athlete_email):
    from etasks import emails

    if user and user.id == listing.club_id and listing.status == 'active':
        if closed_reason in ['found_on_sporple', 'found_elsewhere', 'no_hire']:
            listing.closed_reason = closed_reason
            if closed_reason == 'found_on_sporple' and hired_user_id:
                listing.hired_user_id = int(hired_user_id)
            elif closed_reason == 'found_elsewhere' and athlete_email:
                listing.hired_email = athlete_email

        listing.status = 'closed'
        d.session.commit()
        if closed_reason == 'found_elsewhere' and athlete_email:
            emails.invite_friend.delay(athlete_email, user.id)
    else:
        raise UserWarning("Invalid action, cannot delete listing")


def save_listing(form, listing, profile):
    if listing and profile.user_id != listing.club_id:
        raise UserWarning("Invalid action, cannot edit listing")

    if not listing:
        listing = db.Listing(club_id=profile.user_id)
        d.session.add(listing)
    listing.status = 'active'
    listing.description = form.description.data
    listing.season_start = form.season_start.data
    listing.position = form.position.data
    listing.sport_id = form.position.data.sport_id

    listing.age_min = int(form.age_min.data)
    listing.age_max = int(form.age_max.data)
    listing.height_min = int(form.height_min.data)
    listing.height_max = int(form.height_max.data)
    listing.weight_min = int(form.weight_min.data)
    listing.weight_max = int(form.weight_max.data)
    listing.country_groups = [c for c in form.country_groups.data if c.id]

    d.session.commit()


'''
Listing application.
'''


def save_application(form, listing, profile, role):
    from etasks import emails
    # listing = get_listing(int(listing_id))
    if profile.user.has_applied(listing.id, role):
        raise UserWarning("You cannot apply again")
    if role == "club":
        listing_id = listing.id
        looking_for_id = None
        listing_user_id = listing.club.id
    else:
        listing_id = 23
        looking_for_id = listing.id
        listing_user_id = listing.user.id

    application = db.Application(
        listing_id=listing_id,
        looking_for_id=looking_for_id,
        applicant_id=profile.user_id,
        note=form.note.data)
    d.session.add(application)
    d.session.commit()
    emails.notify_new_application.delay(
        listing_user_id, profile.user_id, application.id)


def get_listings(profile):
    return db.Listing.query.filter_by(club_id=profile.user_id).all()


def is_following(profile_user_id, user_id):
    return bool(db.UserConnection.query
                .filter_by(user_id=user_id)
                .filter_by(other_user_id=profile_user_id)
                .first())


def get_suggested_profiles(sport_id, page=1):
    role = db.Role.query.filter_by(slug='athlete').first()
    query = (db.User.query
             .join(db.User.profile)
             .filter(db.UserProfile.image != None)
             .filter(db.UserProfile.height != None)
             .filter(db.UserProfile.weight != None)
             .filter(db.UserProfile.nationality_id != None)
             .filter(db.UserProfile.personal_statement != None)
             .filter(db.UserProfile.reel_video_url != None)
             .filter(db.UserProfile.role_id == role.id)
             .filter(db.User.positions.any())
             .filter(db.User.career_items.any())
             .order_by(db.User.created_at.desc())
             .limit(20)
             .offset((page - 1) * 20))
    users = query.all()
    return users


def get_related_profiles(profile, page=1, seed=1):
    seed = seed / 100.0
    d.engine.execute('select setseed({0});'.format(seed))
    if not profile.user.sports:
        return []
    conn_query = db.UserConnection.query \
        .with_entities(db.UserConnection.other_user_id) \
        .filter_by(user_id=profile.user_id)
    query = (db.User.query
             .join(db.User.profile)
             .filter(~db.User.id.in_(conn_query))
             .filter(db.User.sports.any(id=profile.user.sport.id))
             .filter(db.UserProfile.image != None)
             .filter(db.UserProfile.role_id == profile.role_id))
    if profile.user.role_slug == 'club':
        query = query.filter(db.UserProfile.club_name != '')
    else:
        query = query.filter(db.UserProfile.firstname != '')
    query = (query
             .order_by(func.random())
             .limit(8)
             .offset((page - 1) * 8))
    users = query.all()
    return users


def get_profile_by_user_id(user_id):
    profile = db.UserProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        raise UserWarning("Invalid user_id")
    return profile


def ensure_slug(name):
    return auth_controller.ensure_slug(name)


def is_user_eligible(listing):
    missing = {}
    profile = current_user.user.profile

    if not profile.address_country_id:
        missing['country'] = 'Country of Residence'
    if not profile.nationality_id:
        missing['nationality'] = 'Nationality'
    if not profile.reel_video_url:
        missing['reel_video'] = 'Player Showreel video'
    if not profile.birthday:
        missing['birthday'] = 'Date of Birth'
    if not profile.height:
        missing['height'] = 'Height'
    if not profile.weight:
        missing['weight'] = 'Weight'
    if not profile.user.career_items:
        missing['career_info'] = 'Career Timeline'

    if not missing:
        if lcontroller.is_eligible(profile, listing):
            return True
        else:
            return False

    complete_percent = 100 - (len(missing) * 5)
    return False


def get_listing_from_role(listing_id, role):
    if role == 'club':
        return get_listing(listing_id)
    else:
        return get_looking_for(listing_id)
