import db
from main import database as d


# make existing listings as active
def make_listings_active(dry_run=True):
    listings = (db.Listing.query.all())
    for l in listings:
        l.status = 'active'
    d.session.commit()
