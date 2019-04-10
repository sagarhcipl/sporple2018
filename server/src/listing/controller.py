import db

from config import sport
from main import app


def get_latest_listing(sport_slug='rugby'):
    sport_id = sport.id_from_slug(sport_slug)

    latest_listings = (db.Listing.query
        .join(db.UserProfile, db.Listing.club_id == db.UserProfile.user_id)
        .filter(db.UserProfile.image.isnot(None))
        .filter(db.Listing.status == 'active')
        .order_by(db.Listing.created_at.desc())
        .limit(6))
    return latest_listings


def get_listings_for_club(club_id=0):
    return (db.Listing.query
        .filter_by(club_id = club_id)
        .filter_by(status='active')
        .order_by(db.Listing.created_at.desc())
        .all())


def get_listings_for_sport(sport_id, page):
    listings = (db.Listing.query
        .join(db.UserProfile, db.Listing.club_id == db.UserProfile.user_id)
        .join(db.Position, db.Listing.position_id == db.Position.id)
        .filter(db.UserProfile.image.isnot(None))
        .filter(db.Position.sport_id == sport_id)
        .filter(db.Listing.status == 'active')
        .order_by(db.Listing.created_at.desc())
        .paginate(page=page, per_page=20, error_out=False)
        .items)
    return listings


def get_listings_for_sports(sports, page):
    sport_ids = [sport.id for sport in sports]
    listings = (db.Listing.query
        .join(db.UserProfile, db.Listing.club_id == db.UserProfile.user_id)
        .join(db.Position, db.Listing.position_id == db.Position.id)
        .filter(db.UserProfile.image.isnot(None))
        .filter(db.Position.sport_id.in_(sport_ids))
        .filter(db.Listing.status == 'active')
        .order_by(db.Listing.created_at.desc())
        .paginate(page=page, per_page=20, error_out=False)
        .items)
    return listings


def is_eligible(profile, listing):
    age = profile.age
    return age and profile.height and profile.weight \
        and profile.address_country_id \
        and profile.nationality_id \
        and profile.reel_video_url \
        and profile.height >= listing.height_min \
        and profile.height <= listing.height_max \
        and profile.weight >= listing.weight_min \
        and profile.weight <= listing.weight_max \
        and age >= listing.age_min \
        and age <= listing.age_max \
        and is_valid_group(profile, listing)

def is_valid_group(profile, listing):
    cgs = listing.country_groups
    if not cgs:
        return True
    cg_ids = [cg.id for cg in cgs]
    if profile.passport_1_id:
        profile_cg_id = profile.passport_1.country_group_id
        if profile_cg_id in cg_ids:
            return True
    if profile.passport_2_id:
        profile_cg_id = profile.passport_2.country_group_id
        if profile_cg_id in cg_ids:
            return True
    return False

