import datetime
import db
from sqlalchemy import and_
from sqlalchemy import or_
from flask.ext.login import current_user
from db import Sport
from main import database as d
from itertools import chain
from operator import attrgetter

def search_opportunity(form, page):
    lquery = db.Listing.query \
        .join(db.UserProfile, db.Listing.club_id == db.UserProfile.user_id) \
        .filter(db.Listing.status == 'active', db.Listing.sport_id == current_user.user.sport.id)
    looking_query = db.LookingFor.query \
        .join(db.UserProfile, db.LookingFor.user_id == db.UserProfile.user_id) \
        .filter(db.LookingFor.sport_id == current_user.user.sport.id)
    countries = form.country.data
    if countries:
        country_ids = [c.id for c in countries if c.id]
        lquery = lquery.filter(db.UserProfile.address_country_id.in_(country_ids))
        looking_query = looking_query.filter(db.UserProfile.address_country_id.in_(country_ids))
    positions = form.positions.data
    if positions:
        position_ids = [p.id for p in positions if p.id]
        lquery = lquery.filter(db.Listing.position_id.in_(position_ids))
        looking_query = looking_query.filter(db.LookingFor.position_id.in_(position_ids))

    tquery = sorted(chain(lquery.all(), looking_query.all()), key=attrgetter('created_at'), reverse=True)
    total = len(tquery)
    next_offset = page + 1
    tquery = tquery[page*10:next_offset*10]

    return tquery, total


def search_advanced(page, params={}):
    sports = params.get('sports')
    type = params.get('type')
    firstname = params.get('firstname')
    lastname = params.get('lastname')
    clubname = params.get('clubname')
    gender = params.get('gender')
    positions = params.get('positions[]')
    countries = params.get('countries[]')
    passports = params.get('passports[]')
    min_age = params.get('age_min')
    max_age = params.get('age_max')
    min_height = params.get('height_min')
    max_height = params.get('height_max')
    min_weight = params.get('weight_min')
    max_weight = params.get('weight_max')
    has_showreel = params.get('has_showreel')
    has_listings = params.get('has_listings')
    has_agent = params.get('has_agent')
    min_exp = params.get('min_experience')
    has_qualifications = params.get('has_qualifications')
    has_clients = params.get('has_clients')
    has_vacancies = params.get('has_vacancies')

    if positions:
        positions = _get_positions(positions)
    if countries:
        countries = _get_countries(countries)
    if passports:
        passports = _get_passports(passports)

    query = db.UserProfile.query \
            .join(db.User, db.User.id == db.UserProfile.user_id)
    if firstname:
        query = query.filter(db.UserProfile.firstname.ilike(firstname))
    if lastname:
        query = query.filter(db.UserProfile.lastname.ilike(lastname))
    if clubname:
        query = query.filter(db.UserProfile.club_name.ilike(clubname))

    if type:
        role = _get_type(type)
        if role:
            query = query.filter(db.UserProfile.role_id == role.id)

    if sports:
        sport = _get_sport(sports)
        if sport:
            query = query.filter(db.User.sports.any(id=sport.id))

    if positions:
        position_queries = []
        for position in positions:
            position_queries.append(db.User.positions.any(id=position.id))
        query = query.filter(or_(*position_queries))

    if countries:
        country_ids = [c.id for c in countries if c.id]
        query = query.filter(db.UserProfile.address_country_id.in_(country_ids))
    if passports:
        passport_ids = [p.id for p in passports if p.id]
        query = query.filter(or_(db.UserProfile.passport_1_id.in_(passport_ids), \
                db.UserProfile.passport_2_id.in_(passport_ids)))

    if gender != None:
        query = query.filter(db.UserProfile.gender == (0 if gender == 'male' else 1))

    if has_showreel:
        query = query.filter(and_(db.UserProfile.reel_video_url != '', db.UserProfile.reel_video_url is not None))

    if has_listings:
        query = query.filter(db.User.listings.any())

    today = datetime.date.today()
    if min_age:
        max_bday = today.replace(year=today.year - int(min_age))
        query = query.filter(db.UserProfile.birthday < max_bday)
    if max_age:
        min_bday = today.replace(year=today.year - int(max_age))
        query = query.filter(db.UserProfile.birthday > min_bday)

    if max_height:
        query = query.filter(db.UserProfile.height <= int(max_height))
    if min_height:
        query = query.filter(db.UserProfile.height >= int(min_height))

    if max_weight:
        query = query.filter(db.UserProfile.weight <= int(max_weight))
    if min_weight:
        query = query.filter(db.UserProfile.weight >= int(min_weight))

    if min_exp:
        query = query.filter(db.UserProfile.years_experience >= int(min_exp))

    if has_qualifications:
        query = query.filter(db.User.qualifications.any())

    if has_clients:
        query = query.filter(db.User.clients.any())

    return query.order_by(db.UserProfile.created_at.desc()) \
        .offset(page*10).limit(10), query.count()


def _get_countries(countries):
    if not isinstance(countries, list):
        countries = [countries]
    return db.Country.query.filter(db.Country.name.in_(countries)).all()


def _get_positions(positions):
    if not isinstance(positions, list):
        positions = [positions]
    return db.Position.query.filter(db.Position.name.in_(positions)).all()


def _get_passports(passports):
    if not isinstance(passports, list):
        passports = [passports]
    return db.Nationality.query.filter(db.Nationality.name.in_(passports)).all()

def _get_type(type):
    return db.Role.query.filter_by(slug=type).first()

def _get_sport(sports):
    return db.Sport.query.filter_by(slug=sports).first()

