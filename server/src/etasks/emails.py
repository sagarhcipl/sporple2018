import braintree
import datetime
import db
import email_templates
import logging
import mandrill
from config import sport
from config import plan
from flask import render_template
from flask import url_for
from main import app
from main import celery
from relate import config as relate_config


@celery.task()
def notify_new_follower(user_id, follower_id):
    user = db.User.query.get(user_id) 
    follower = db.User.query.get(follower_id)

    email_preferences = (db.UserEmailPreference.query
            .filter_by(user_id=user.id)
            .first())
    if user.unclaimed:
        return
    if not email_preferences or email_preferences.new_follower:
        _send_email('notify_new_follower',
                params={'user': user, 'follower': follower},
                to_email=_to_email(user),
                to_name=user.name)


@celery.task()
def notify_post_like(post_id, liker_id):
    post = db.Post.query.get(post_id)
    liker = db.User.query.get(liker_id)

    email_preferences = (db.UserEmailPreference.query
            .filter_by(user_id=post.user.id)
            .first())

    if post.user.unclaimed:
        return

    if not email_preferences or email_preferences.new_post_like:
        _send_email('notify_post_like',
                params={
                    'user': post.user,
                    'liker': liker,
                    'post': post
                },
                to_email=_to_email(post.user),
                to_name=post.user.name)


@celery.task()
def notify_new_message(user_id, sender_id, message_id):
    user = db.User.query.get(user_id)
    sender = db.User.query.get(sender_id)
    message = db.Message.query.get(message_id)
    message_thread_user = (db.MessageThreadUser.query
            .filter_by(thread_id=message.thread_id)
            .filter_by(user_id=user_id)
            .first())
    if not message_thread_user or not message_thread_user.nb_unread_messages:
        # If message is already read, don't send notification
        return
    if user.unclaimed:
        return
 
    email_preferences = (db.UserEmailPreference.query
            .filter_by(user_id=user.id)
            .first())

    if not email_preferences or email_preferences.new_message:
        _send_email('notify_new_message',
            params={
                'user': user,
                'sender': sender,
                'message': message
            },
            to_email=_to_email(user),
            to_name=user.name)


@celery.task()
def notify_new_application(club_id, applicant_id, application_id):
    club = db.User.query.get(club_id)
    applicant = db.User.query.get(applicant_id)
    application = db.Application.query.filter_by(id=application_id).first()

    email_preferences = (db.UserEmailPreference.query
            .filter_by(user_id=club.id)
            .first())

    if club.unclaimed:
        return
 
    if not email_preferences or email_preferences.new_application:
        _send_email('notify_new_application',
            params={
                'club': club,
                'applicant': applicant,
                'application': application
            },
            to_email=club.username,
            to_name=club.name)


@celery.task()
def notify_post_share(user_id, post_id, sharer_id):
    user = db.User.query.get(user_id)
    post = db.Post.query.get(post_id)
    sharer = db.User.query.get(sharer_id)

    email_preferences = (db.UserEmailPreference.query
            .filter_by(user_id=user.id)
            .first())

    if user.unclaimed:
        return

    if not email_preferences or email_preferences.new_post_share:
        _send_email('notify_post_share',
            params={
                'user': user,
                'post': post,
                'sharer': sharer
            },
        to_email=_to_email(user),
        to_name=user.name)


@celery.task()
def notify_comment(user_id, post_id, comment_id, commenter_id):
    user = db.User.query.get(user_id)
    post = db.Post.query.get(post_id)
    comment = db.Comment.query.get(comment_id)
    commenter = db.User.query.get(commenter_id)

    if user.unclaimed:
        return
 
    email_preferences = (db.UserEmailPreference.query
            .filter_by(user_id=user.id)
            .first())

    if not email_preferences or email_preferences.new_post_message:
        _send_email('notify_comment',
            params={
                'user': user,
                'post': post,
                'comment': comment,
                'commenter': commenter
            },
            to_email=_to_email(user),
            to_name=user.name)


@celery.task()
def notify_new_relation(relation_type, user_id, source_user_id):
    user = db.User.query.get(user_id) 
    source_user = db.User.query.get(source_user_id)

    if user.unclaimed:
        return

    email_preferences = (db.UserEmailPreference.query
            .filter_by(user_id=user.id)
            .first())
    if not email_preferences or email_preferences.new_follower:
        relate_info = relate_config.get(relation_type)
        relation_desc = relate_info['email_desc'] % {
                'source_user_name': source_user.name
        }
        _send_email('notify_new_relation',
                params={
                    'user': user,
                    'source_user': source_user,
                    'source_user_name': source_user.name,
                    'relation_desc': relation_desc,
                    'relation_type': relation_type},
                to_email=_to_email(user),
                to_name=user.name)


@celery.task()
def engage_inactive_agent(agent_id):
    user = db.User.query.get(agent_id)
    sport_twitter = ''

    if user.unclaimed:
        return
 
    if user.sport:
        sport_twitter = sport.get(user.sport_slug).get('twitter')
    _send_email('engage_inactive_agent',
        params={
            'user': user,
            'sporple_sport_twitter': sport_twitter
        },
        to_email=user.username,
        to_name=user.name)


@celery.task()
def engage_inactive_athlete(athlete_id):
    user = db.User.query.get(athlete_id)
    sport_twitter = ''

    if user.unclaimed:
        return

    if user.sport:
        sport_twitter = sport.get(user.sport_slug).get('twitter')
    _send_email('engage_inactive_athlete',
        params={
            'user': user,
            'sporple_sport_twitter': sport_twitter
        },
        to_email=user.username,
        to_name=user.name)


@celery.task()
def engage_inactive_club(club_id):
    user = db.User.query.get(club_id)
    sport_twitter = ''

    if user.unclaimed:
        return
 
    if user.sport:
        sport_twitter = sport.get(user.sport_slug).get('twitter')
    _send_email('engage_inactive_club',
        params={
            'user': user,
            'sporple_sport_twitter': sport_twitter
        },
        to_email=user.username,
        to_name=user.name)


@celery.task()
def forgot_password(user_id, token):
    user = db.User.query.get(user_id)

    if user.unclaimed:
        return
 
    reset_password_url = url_for('reset_password',
        sig=token, username=user.username, _external=True)
    _send_email('forgot_password',
        params={
            'user': user,
            'reset_password_url': reset_password_url
        },
        to_email=user.username,
        to_name=user.name)


@celery.task()
def subscription_invoice(subscription_id):
    subscription = db.UserSubscription.query.get(subscription_id)
    bt_subscription = braintree.Subscription.find(subscription.braintree_subscription_id)
    user = subscription.user
    role_slug = user.role_slug
    plan_info = plan.get(role_slug, subscription.plan_type)
    _send_email('subscription_invoice',
        params={
            'user': user,
            'subscription': subscription,
            'bt_subscription': bt_subscription,
            'plan': plan_info,
            'role_slug': role_slug,
        },
        to_email=user.username,
        to_name=user.name)


@celery.task()
def send_daily_report(params):
    to = app.config['ADMIN_EMAILS']
    _send_email('daily_report', params=params, to=to)


@celery.task()
def send_weekly_report(params):
    to = app.config['ADMIN_EMAILS']
    _send_email('weekly_report', params=params, to=to)


@celery.task()
def send_recommendations_club(club, profiles):
    email_preferences = (db.UserEmailPreference.query
            .filter_by(user_id=club.id)
            .first())

    if club.unclaimed:
        return
 
    if not email_preferences or email_preferences.recommendations:
        _send_email('recommendations_club',
            params={
                'user': club,
                'profiles': profiles,
                'today': datetime.date.today().strftime('%b %d'),
            },
            to_email=club.username,
            to_name=club.name)


@celery.task()
def send_recommendations_agent(agent, profiles):
    email_preferences = (db.UserEmailPreference.query
            .filter_by(user_id=agent.id)
            .first())

    if agent.unclaimed:
        return
 
    if not email_preferences or email_preferences.recommendations:
        _send_email('recommendations_agent',
            params={
                'user': agent,
                'profiles': profiles,
                'today': datetime.date.today().strftime('%b %d'),
            },
            to_email=agent.username,
            to_name=agent.name)


@celery.task()
def send_opportunities_athlete(athlete_id, listing_ids):
    email_preferences = (db.UserEmailPreference.query
            .filter_by(user_id=athlete_id)
            .first())
 
    if not email_preferences or email_preferences.recommendations:
        athlete = db.User.query.get(athlete_id)
        if athlete.profile.managed_by_id:
            # Do not send recommendations if it's a managed account
            return

        if athlete.unclaimed:
            return

        listings = [db.Listing.query.filter_by(id=lid).first() for lid in listing_ids]
        _send_email('opportunities_athlete',
            params={
                'user': athlete,
                'listings': listings,
                'today': datetime.date.today().strftime('%b %d'),
            },
            to_email=athlete.username,
            to_name=athlete.name)


@celery.task()
def send_no_listing(club):
    email_preferences = (db.UserEmailPreference.query
            .filter_by(user_id=athlete.id)
            .first())

    if club.unclaimed:
        return

    if not email_preferences or email_preferences.reminders:
        _send_email('club_no_listings',
            params={
                'user': club,
                'today': datetime.date.today().strftime('%b %d'),
            },
            to_email=club.username,
            to_name=club.name)


@celery.task()
def send_incomplete_athlete(athlete):
    email_preferences = (db.UserEmailPreference.query
            .filter_by(user_id=athlete.id)
            .first())

    if athlete.unclaimed:
        return

    if not email_preferences or email_preferences.reminders:
        _send_email('incomplete_athlete',
            params={
                'user': athlete,
                'today': datetime.date.today().strftime('%b %d'),
            },
            to_email=athlete.username,
            to_name=athlete.name)


@celery.task()
def send_not_looking(agent):
    email_preferences = (db.UserEmailPreference.query
            .filter_by(user_id=agent.id)
            .first())

    if agent.unclaimed:
        return

    if not email_preferences or email_preferences.reminders:
        _send_email('agent_not_looking',
            params={
                'user': agent,
                'today': datetime.date.today().strftime('%b %d'),
            },
            to_email=agent.username,
            to_name=agent.name)


@celery.task()
def send_claim_request(claim_id):
    claim = db.ClaimProfile.query.get(claim_id)
    profile = db.UserProfile.query.get(claim.user_id)
    to = app.config['ADMIN_EMAILS']
    _send_email('send_claim_request', params={'claim': claim, 'profile': profile}, to=to)


@celery.task()
def invite_friend(email, user_id):
    user = db.User.query.get(user_id)
    _send_email('invite_friend',
        params={
            'name': user.name,
            'user': user,
        },
        to_email=email,
        to_name=email)


@celery.task()
def welcome(user_id):
    pass


def _send_email(template_name,
        params={},
        to_email='',
        to_name='',
        from_email=app.config['BASE_EMAIL'],
        from_name=app.config['BASE_FROM_NAME'],
        to=[]):

    template = email_templates.MAP.get(template_name)
    if not template:
        logging.error("Invalid template_name: " + template_name)
        return

    if to_email and '@' not in to_email:
        logging.error("No email-address:" + to_email)
        return

    html_template = render_template(template.get('html_template'), **params)
    subject = template.get('subject') % params

    logging.debug('>>>>>>>>>>>>>> SENDING EMAIL TO: ' + to_email + '<<<<<<<<<<')
    logging.debug('SUBJECT: ' + subject)
    logging.debug('>>>>>>>>>>>>>> html email: <<<<<<<<<<<<<<<<<<<<<<<<')
    logging.debug(html_template)
    if not to:
        to = [{'email': to_email, 'name': to_name, 'type': 'to'}]
    try:
        client = mandrill.Mandrill(app.config['MANDRILL_API_KEY'])
        message = {
            'auto_html': None,
            'auto_text': True,
            'bcc_address': app.config['BCC_EMAIL'],
            'from_email': from_email,
            'from_name': from_name,
            'subject': subject,
            'html': html_template,
            'to': to,
            'track_clicks': True,
            'track_opens': True,
        }
        result = client.messages.send(message=message)
        if result[0]['status'] in ['rejected', 'invalid']:
            logging.error('Message sending failed with status: %s, %s'
                % (result[0]['status'], result[0].get('reject_reason', '')))
    except mandrill.Error, e:
        # Mandrill errors are thrown as exceptions
        logging.error('A mandrill error occurred: %s - %s' % (e.__class__, e))


def _to_email(user):
    if user.profile.managed_by_id:
        return user.profile.managed_by.username
    else:
        return user.username
