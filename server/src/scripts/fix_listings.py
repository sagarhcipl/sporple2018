import db
from main import database as d


# Old listings are broken, set the default values for filters.
def fix_listings(dry_run=True):
    listings = (db.Listing.query.all())
    for l in listings:
        if l.height_min is None:
            l.height_min = 0
            print "changed_height_min", l.id
        if l.height_max is None:
            l.height_max = 999
            print "changed_height_max", l.id
        if l.weight_min is None:
            l.weight_min = 0
            print "changed weight_min", l.id
        if l.weight_max is None:
            l.weight_max = 999
            print "changed_weight_max", l.id
        if l.age_min is None:
            l.age_min = 0
            print "change age_min", l.id
        if l.age_max is None:
            l.age_max = 99
            print "changed_age_max", l.id
    if not dry_run:
        d.session.commit()
