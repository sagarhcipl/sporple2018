CLUB = {
    'intro': {
        'price_cents': {
            'monthly':      0,
            'annual':       0,
        },
        'name':             'Basic',
    },
    'pro': {
        'price_cents': {
            'monthly':      29,
            'annual':       300, # $29/month

        },
        'name':             'Premium',
        'monthly_plan_id':     'club_monthly_pro_1',
        'annual_plan_id':      'club_annual_pro_1',
    }
}

AGENT = {
    'intro': {
        'price_cents': {
            'monthly':      0,
            'annual':       0,
        },
        'name':             'Basic',
    },
    'pro': {
        'price_cents': {
            'monthly':      49,
            'annual':       500, # $49/month
        },
        'name':             'Premium',
        'monthly_plan_id':     'agent_monthly_pro_1',
        'annual_plan_id':      'agent_annual_pro_1',
    }
}

ATHLETE = {
    'intro': {
        'price_cents': {
            'monthly':    0,
            'annual':     0,
        },
        'name':             'Basic',
    }
}

def get(role_slug, plan_type):
    if not plan_type:
        plan_type = 'intro'
    if role_slug == 'club' and CLUB.get(plan_type):
        return CLUB.get(plan_type)
    elif role_slug == 'agent' and AGENT.get(plan_type):
        return AGENT.get(plan_type)
    elif role_slug == 'athlete' and ATHLETE.get(plan_type):
        return ATHLETE.get(plan_type)
    else:
        raise UserWarning("Invalid role_slug: " + role_slug + ", plan_type: " + plan_type)
