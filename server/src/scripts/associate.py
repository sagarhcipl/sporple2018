from main import app
import db



def find_clubs():
    found = 0
    not_found = 0
    career_items = db.CareerItem.query.all()
    for ci in career_items:
        if ci.club_name:
            club = db.UserProfile.query.filter_by(club_name=ci.club_name).first()
            if club:
                print "CLUB FOUND", ci.club_name
                found += 1
            else:
                print "NOT FOUND", ci.club_name
                not_found += 1

    print "Total found:", found, "Not Found:", not_found

