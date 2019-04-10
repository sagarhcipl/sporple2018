MAP = {
    'current_team': {
        'email_desc': '%(source_user_name)s has added you to the current team.',
    },
    'past_team': {
        'email_desc': '%(source_user_name)s has added you to the past team.',
    },
    'played_with': {
        'email_desc': '%(source_user_name)s has played with you in past.',
    },
    'current_play_with': {
        'email_desc': '%(source_user_name)s currently plays with you.',
    },
    'want_to_play_with': {
        'email_desc': '%(source_user_name)s wants to play with you.',
    },
    'current_client': {
        'email_desc': '%(source_user_name)s has added you as a current client.',
    },
    'past_client': {
        'email_desc': '%(source_user_name)s has added you as a past client.',
    },
    'want_to_join': {
        'email_desc': '%(source_user_name)s wants to join your team.',
    },
    'want_to_recruit': {
        'email_desc': '%(source_user_name)s wants to recruit you.',
    },
    'want_to_offer': {
        'email_desc': '%(source_user_name)s wants to offer you a job opportunity.',
    },
    'want_to_be_managed': {
        'email_desc': '%(source_user_name)s wants to be managed by you',
    },
    'is_fan': {
        'email_desc': '%(source_user_name)s is your fan!',
    },
    'just_follow': {
        'email_desc': '%(source_user_name)s is now following you',
    },
}

def get(type):
    return MAP.get(type)


def get_all():
    return MAP.keys()

