import db
from main import database as d


groups = {
    'British':          ['British', 'Irish', 'Scottish', 'Welsh'],
    'Other European':   ['Austrian', 'Belgian', 'Bulgarian', 'Croatian',
                         'Cypriot', 'Czech', 'Danish', 'Estonian', 'Finnish', 'French',
                         'German', 'Greek', 'Hungarian', 'Italian', 'Latvian', 'Lithuanian',
                         'Luxembourger', 'Maltese', 'Dutch', 'Polish', 'Portuguese', 'Romanian',
                         'Slovakian', 'Slovenian', 'Spanish', 'Swedish'],
    'Australian':       ['Australian'],
    'New Zealander':    ['New Zealander'],
    'Argentinean':      ['Argentinean'],
    'Georgian':         ['Georgian'],
    'Samoan':           ['Samoan'],
    'Tongan':           ['Tongan'],
    'Fijian':           ['Fijian'],
    'South African':    ['South African'],
    'American':         ['American'],
    'Canadian':         ['Canadian'],
    'Papua New Guinean':['Papua New Guinean'],
    'Asian':            ['Chinese', 'Japanese', 'Indian', 'Thai', 'Filipino', 'Kazakhstani',
                         'Malaysian', 'Singaporean', 'South Korean', 'Sri Lankan', 'Taiwanese',
                         'Pakistani', 'Cambodian', 'Kyrgyz', 'Laotian'],
    'Other':            [],
}

def set_groups():
    for group in groups:
        cg = db.CountryGroup(name=group)
        d.session.add(cg)
        d.session.commit()
        for c in groups[group]:
            country = get_country(c)
            if not country:
                print c, "not found"
            country.country_group_id = cg.id
        d.session.commit()

def get_country(name):
    return db.Nationality.query.filter_by(name=name).first()
