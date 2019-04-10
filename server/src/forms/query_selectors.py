import db
from datetime import date


def country():
    return db.Country.query


def nationality():
    return db.Nationality.query


def sport():
    return db.Sport.query


def country_list(blank=False):
    countries = db.Country.query.all()
    if blank:
        countries = [db.Country(id='', name='Choose Countries(s)')] + countries
    return countries

def country_group_list(blank=False):
    country_groups = db.CountryGroup.query.all()
    if blank:
        country_groups = [db.CountryGroup(id='', name='Choose Country Group(s)')] + country_groups
    return country_groups

def sport_list(blank=False):
    sports = db.Sport.query.all()
    if blank:
        sports = [db.Sport(id='', name='Choose Your sport', slug='')] + sports
    return sports

def marital_status():
    return db.MaritalStatus.query

def user_position_list(sport_id, blank=False):
    positions = db.Position.query.filter_by(sport_id=sport_id).all()
    if blank:
        positions = [db.Position(id='', name='Choose position(s)', slug='')] + positions
    return positions

def role():
    return db.Role.query

def months():
    return [('', 'Month'), ('1', 'Jan'), ('2', 'Feb'), ('3', 'Mar'), ('4', 'Apr'),
        ('5', 'May'),('6', 'Jun'), ('7', 'Jul'), ('8', 'Aug'), ('9', 'Sep'),
        ('10', 'Oct'), ('11', 'Nov'), ('12', 'Dec')]

def years():
    return [('', 'Year')] + [(str(x), x) for x in reversed(range(1950, date.today().year + 1))]
