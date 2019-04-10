MAP = {
    'notify_new_follower': {
        'subject': 'You have a new follower!',
        'html_template': 'emails/notify_new_follower.html',
    },

    'notify_post_like': {
        'subject': 'You have a new like!',
        'html_template': 'emails/notify_post_like.html',
    },

    'notify_new_message': {
        'subject': 'You have a new message!',
        'html_template': 'emails/notify_new_message.html',
    },

    'notify_new_application': {
        'subject': 'You have a new applicant!',
        'html_template': 'emails/notify_new_application.html',
    },

    'notify_post_share': {
        'subject': 'Someone shared your post',
        'html_template': 'emails/notify_post_share.html',
    },

    'notify_comment': {
        'subject': 'You have a new comment',
        'html_template': 'emails/notify_comment.html',
    },

    'engage_inactive_agent': {
        'subject': 'Don\'t miss these new players!',
        'html_template': 'emails/engage_inactive_agent.html',
    },

    'engage_inactive_athlete': {
        'subject': 'A lot has happened since you\'ve been away!',
        'html_template': 'emails/engage_inactive_athlete.html',
    },

    'engage_inactive_club': {
        'subject': 'Don\'t miss these new players!',
        'html_template': 'emails/engage_inactive_club.html',
    },

    'forgot_password': {
        'subject': 'Forgot password request',
        'html_template': 'emails/forgot_password.html',
    },
    'subscription_invoice': {
        'subject': 'Invoice for Premium Membership',
        'html_template': 'emails/subscription_invoice.html',
    },
    'daily_report': {
        'subject': 'Sporple Daily Metrics - %(duration)s',
        'html_template': 'emails/report.html',
    },
    'weekly_report': {
        'subject': 'Sporple Weekly Metrics - %(duration)s',
        'html_template': 'emails/report.html',
    },
    'recommendations_club': {
        'subject': 'Athletes looking for opportunities - %(today)s',
        'html_template': 'emails/recommendations_club.html',
    },
    'recommendations_agent': {
        'subject': 'Athletes looking for opportunities - %(today)s',
        'html_template': 'emails/recommendations_agent.html',
    },
    'opportunities_athlete': {
        'subject': 'Clubs looking for athletes like you -  %(today)s',
        'html_template': 'emails/opportunities_athlete.html',
    },
    'club_no_listings': {
        'subject': 'Post opportunities and recruit for free - %(today)s',
        'html_template': 'emails/club_no_listings.html',
    },
    'agent_not_looking': {
        'subject': 'Post opportunities and recruit for free - %(today)s',
        'html_template': 'emails/agent_not_looking.html',
    },
    'notify_new_relation': {
        'subject': '%(source_user_name)s is now connected to you',
        'html_template': 'emails/notify_new_relation.html',
    },
    'send_claim_request': {
        'subject': 'New Claim Request',
        'html_template': 'emails/send_claim_request.html',
    },
    'invite_friend': {
        'subject': '%(name)s invited you to join Sporple',
        'html_template': 'emails/invite_friend.html',
    },

    'welcome': {
        'subject': '',
        'html_template': 'emails/welcome.html',
    }
}
