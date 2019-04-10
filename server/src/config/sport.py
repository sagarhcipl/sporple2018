
SPORT_MAP = {
    'football': {
        'slug': 'football',
        'id': 1,
        'name': 'Football',
        'twitter': 'sporplefootball',
    },
    'rugby': {
        'slug': 'rugby',
        'id': 2,
        'name': 'Rugby',
        'twitter': 'sporplerugby',
    },
    'baseball': {
        'slug': 'baseball',
        'id': 3,
        'name': 'Baseball',
        'twitter': 'sporplebball',
    },
    'basketball': {
        'slug': 'basketball',
        'id': 4,
        'name': 'Basketball',
        'twitter': 'Sporple',
    }
}

def id_from_slug(slug):
    sport = SPORT_MAP.get(slug)
    if not sport:
        raise UserWarning("Invalid sport")
    return sport.get('id')


def get(slug):
    return SPORT_MAP.get(slug)
