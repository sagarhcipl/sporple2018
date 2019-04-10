ROLE_MAP = {
    'agent': {
        'id': 1,
        'slug': 'agent',
        'name': 'Agent',
    },
    'athlete': {
        'id': 2,
        'slug': 'athlete',
        'name': 'Athlete',
    },
    'club': {
        'id': 3,
        'slug': 'club',
        'name': 'Club',
    },
}


def id_from_slug(slug):
    role = ROLE_MAP.get(slug)
    if not role:
        raise UserWarning("Invalid Role")
    return role.get('id')


def get(slug):
    return ROLE_MAP.get(slug)
