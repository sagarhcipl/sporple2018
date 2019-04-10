from main import app
from main import views as main
from auth import views as auth
from flask import redirect
from flask import send_from_directory
from profile import views as profile
from social import views as social
from message import views as message
from payment import views as payment
from relate import views as relate
from search import views as search
from settings import views as settings
from stats import views as stats
from uploads import views as uploads

'''
Routes for Dev and Staging when not served from CDN
'''
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(app.static_folder + '/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(app.static_folder + '/css', path)

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory(app.static_folder + '/images', path)

@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory(app.static_folder + '/fonts', path)

@app.route('/apple-touch-icon-120x120.png')
def apple_touch_icon_large():
    return send_images('apple-touch-icon-120x120.png')

@app.route('/apple-touch-icon.png')
def apple_touch_icon_regular():
    return send_images('apple-touch-icon.png')

@app.route('/apple-touch-icon-120x120-precomposed.png')
def apple_touch_icon_precomposed():
    return apple_touch_icon_large()

@app.route('/apple-touch-icon-precomposed.png')
def apple_touch_icon_regular_precomposed():
    return apple_touch_icon_regular()

@app.route('/about')
def about_us():
    return redirect('https://newsroom.sporple.com/about-us')

METHODS_ALL = ['GET', 'POST']
GET = ['GET']
POST = ['POST']

app.add_url_rule('/uploads/<path:path>',
                 'uploads.proxy',
                 uploads.proxy,
                 methods=GET)

app.add_url_rule('/',
                 'index',
                 main.index,
                 methods=METHODS_ALL)

app.add_url_rule('/favicon.ico', view_func=main.favicon)

app.add_url_rule('/robots.txt', view_func=main.robots_txt)
# Auth & Registration
app.add_url_rule('/login',
                 'login',
                 view_func=auth.login,
                methods=METHODS_ALL)

app.add_url_rule('/signin',
                 'signin',
                 view_func=auth.login_page,
                 methods=GET)

app.add_url_rule('/login_as/<slug>',
                 view_func=auth.login_as,
                 methods=GET)

app.add_url_rule('/logout',
                 'logout',
                 auth.logout,
                 methods=METHODS_ALL)

app.add_url_rule('/forgot_password',
                 'forgot_password',
                 auth.forgot_password,
                 methods=METHODS_ALL)

app.add_url_rule('/reset_password',
                 'reset_password',
                 auth.reset_password,
                 methods=METHODS_ALL)

app.add_url_rule('/facebook_authorize',
                 'facebook_authorize',
                 auth.facebook_authorize,
                 methods=METHODS_ALL)

app.add_url_rule('/registration/congratulations',
                 'registration_congratulations',
                 auth.registration_congratulations,
                 methods=METHODS_ALL)

app.add_url_rule('/register',
                 'register',
                 auth.register,
                 methods=METHODS_ALL,
                 defaults={'sport': None})

app.add_url_rule('/register/<sport>',
                 'register_sport',
                 auth.register,
                 methods=METHODS_ALL)

app.add_url_rule('/register/json',
                 'register.json',
                 auth.register_json,
                 methods=POST)

app.add_url_rule('/register_info',
                 'register_info',
                 auth.register_info,
                 methods=METHODS_ALL)

app.add_url_rule('/upload_attachment',
                 'upload.attachment',
                 uploads.attachment,
                 methods=POST)

app.add_url_rule('/attachment/delete/<attachment_id>',
                 'upload.delete',
                 uploads.delete_attachment,
                 methods=METHODS_ALL)

app.add_url_rule('/auto_register_club',
                 'auth.auto_register_club',
                 auth.auto_register_club,
                 methods=METHODS_ALL)

app.add_url_rule('/auto_register_athlete',
                 'auth.auto_register_athlete',
                auth.auto_register_athlete,
                methods=METHODS_ALL)

app.add_url_rule('/claim_profile/<user_id>',
                 'auth.claim_profile',
                 auth.claim_profile,
                 methods=METHODS_ALL)

app.add_url_rule('/approve_claim/<claim_id>',
                 'auth.approve_claim',
                 auth.approve_claim,
                 methods=GET)

app.add_url_rule('/invite',
                 'auth.invite',
                 auth.invite_friends,
                 methods=METHODS_ALL)

#Profile
app.add_url_rule('/profile/clearField/<path:path>',
                 'profile.clear_field',
                 profile.clear_field,
                 methods=METHODS_ALL)

app.add_url_rule('/profile/relatedProfiles',
                 'profile.related_profiles',
                 profile.related_profiles,
                 methods=METHODS_ALL)

app.add_url_rule('/profile/<user_id>',
                 'profile.main',
                 profile.main,
                 methods=['GET'])

app.add_url_rule('/profile_edit/basic_athlete_information',
                 'profile.edit_athlete',
                 profile.edit_basic_athlete,
                 methods=METHODS_ALL)


app.add_url_rule('/profile_edit/basic_agent_information',
                 'profile.edit_agent',
                 profile.edit_basic_agent,
                 methods=METHODS_ALL)

app.add_url_rule('/profile_edit/basic_club_information',
                 'profile.edit_club',
                 profile.edit_basic_club,
                 methods=METHODS_ALL)

app.add_url_rule('/profile/upload_photo',
                 'profile.upload_photo',
                 profile.upload_profile_photo,
                 methods=POST)

app.add_url_rule('/profile/player_media',
                 view_func=profile.view_player_media,
                 methods=GET)

app.add_url_rule('/profile_edit/player_media',
                 'profile.edit_player_media',
                 view_func=profile.player_media,
                 methods=METHODS_ALL)

app.add_url_rule('/profile_edit/club_media',
                 view_func=profile.player_media,
                 methods=METHODS_ALL)

app.add_url_rule('/profile/player_media_thumb/edit',
                 'profile.edit_media_thumb',
                 view_func=profile.player_media_thumb,
                 methods=METHODS_ALL)

app.add_url_rule('/profile_edit/personal_statement',
                 'profile.edit_personal_statement',
                 view_func=profile.edit_personal_statement,
                 methods=METHODS_ALL)

app.add_url_rule('/profile_edit/career_summary',
                 'profile.edit_career_summary',
                 view_func=profile.edit_career_summary,
                 methods=METHODS_ALL)

app.add_url_rule('/achievement/delete/<id>',
                 'profile.delete_achievement',
                 profile.delete_achievement,
                 methods=METHODS_ALL)

app.add_url_rule('/profile_edit/achievement',
                 'profile.edit_achievement',
                 profile.edit_achievement,
                 methods=METHODS_ALL,
                 defaults={'id': None})

app.add_url_rule('/profile_edit/achievement/<id>',
                 'profile.edit_achievement_id',
                 profile.edit_achievement,
                 methods=METHODS_ALL)

app.add_url_rule('/careeritem/delete/<id>',
                 'profile.delete_career_item',
                 profile.delete_career_item,
                 methods=METHODS_ALL)

app.add_url_rule('/profile_edit/career_item',
                 'profile.edit_career_item',
                 profile.edit_career_item,
                 methods=METHODS_ALL,
                 defaults={'id': None})

app.add_url_rule('/profile_edit/career_item/<id>',
                 'profile.edit_career_item_id',
                 view_func=profile.edit_career_item,
                 methods=METHODS_ALL)

app.add_url_rule('/profile/edit_endorsement',
                 'profile.edit_endorsement',
                 profile.edit_endorsement,
                 methods=METHODS_ALL,
                 defaults={'id': None})

app.add_url_rule('/profile_edit/endorsement/<id>',
                 'profile.edit_endorsement_id',
                 profile.edit_endorsement,
                 methods=METHODS_ALL)

app.add_url_rule('/endorsement/delete/<id>',
                 'profile.delete_endorsement',
                 profile.delete_endorsement,
                 methods=METHODS_ALL)

app.add_url_rule('/profile/edit_qualification',
                 'profile.edit_qualification',
                 view_func=profile.edit_qualification,
                 methods=METHODS_ALL,
                 defaults={'id': None})

app.add_url_rule('/profile_edit/qualification/<id>',
                 'profile.edit_qualification_id',
                 view_func=profile.edit_qualification,
                 methods=METHODS_ALL)


app.add_url_rule('/qualification/delete/<id>',
                 'profile.delete_qualification',
                  profile.delete_qualification,
                  methods=POST)

app.add_url_rule('/profile_edit/club_about',
                 'profile.edit_club_about',
                 view_func=profile.edit_club_about,
                 methods=METHODS_ALL)

app.add_url_rule('/profile/edit_client',
                 'profile.edit_client',
                  view_func=profile.edit_client,
                  methods=METHODS_ALL,
                  defaults={'id': None})

app.add_url_rule('/profile_edit/client/<id>',
                 'profile.edit_client_id',
                 view_func=profile.edit_client,
                 methods=METHODS_ALL)

app.add_url_rule('/profile/delete_client/<id>',
                 'profile.delete_client',
                  view_func=profile.delete_client,
                  methods=METHODS_ALL)

app.add_url_rule('/profile/clients',
                  'profile.clients',
                  view_func=profile.clients,
                  methods=GET)

app.add_url_rule('/profile/new_looking_for',
                 'profile.new_looking_for',
                 view_func=profile.edit_looking_for,
                 methods=METHODS_ALL,
                 defaults={'id': None})

app.add_url_rule('/profile_edit/looking_for/<id>',
                 'profile.edit_looking_for',
                 view_func=profile.edit_looking_for,
                 methods=METHODS_ALL)

app.add_url_rule('/profile/delete_looking_for/<id>',
                 'profile.delete_looking_for',
                 view_func=profile.delete_looking_for,
                 methods=METHODS_ALL)

app.add_url_rule('/profile/looking_for_list',
                 'profile.looking_for_list',
                 view_func=profile.looking_for_list,
                 methods=GET)

app.add_url_rule('/profile/show_looking_for',
                 'profile.show_looking_for',
                 view_func=profile.show_looking_for,
                 methods=GET)

app.add_url_rule('/profile_edit/twitter',
                 'profile.twitter_account',
                 view_func=profile.twitter_account,
                 methods=METHODS_ALL)

app.add_url_rule('/<slug>',
                 'profile.slug',
                 profile.slug,
                 methods=METHODS_ALL)

app.add_url_rule('/<sport>/<slug>',
                 'profile.sport_slug',
                 view_func=profile.sport_slug,
                 methods=METHODS_ALL)

app.add_url_rule('/can_apply/<listing_id>/<role>', view_func=profile.can_apply)
app.add_url_rule('/applicant-list/',
                 'profile.get_applicant_list',
                 view_func=profile.get_applicant_list,
                 methods=METHODS_ALL)

# Settings
app.add_url_rule('/settings/email_notifications',
                 'settings.email_notifications',
                 view_func=settings.email_notifications,
                 methods=METHODS_ALL)

app.add_url_rule('/settings/password',
                 'settings.password',
                 view_func=settings.password,
                 methods=METHODS_ALL)

app.add_url_rule('/settings/email',
                 'settings.email',
                 view_func=settings.email,
                 methods=METHODS_ALL)


# New Club
app.add_url_rule('/club-listing/edit',
                 'profile.edit_club_listing',
                 profile.edit_club_listing,
                 methods=METHODS_ALL)

app.add_url_rule('/club/delete_listing/<id>',
                 'club.delete_listing',
                 profile.delete_listing,
                 methods=METHODS_ALL)

app.add_url_rule('/application/new',
                 'profile.new_application',
                 profile.new_application,
                 methods=METHODS_ALL)

# Interactions
app.add_url_rule('/post',
                 'post.submit',
                 view_func=social.post,
                 methods=POST)

app.add_url_rule('/post/delete/<id>',
                 'post.delete',
                 view_func=social.post_delete,
                 methods=METHODS_ALL)

app.add_url_rule('/post/list',
                 'post.list',
                 view_func=social.post_list,
                 methods=METHODS_ALL)

app.add_url_rule('/post/comment',
                 'post.comment',
                 view_func=social.post_comment,
                 methods=METHODS_ALL)

app.add_url_rule('/post/favourite',
                 'post.favourite',
                 view_func=social.favourite_post,
                 methods=GET)

app.add_url_rule('/post/unfavourite',
                 'post.unfavourite',
                 view_func=social.unfavourite_post,
                 methods=GET)

app.add_url_rule('/connections',
                 'connections',
                 view_func=social.connections,
                 methods=METHODS_ALL)


app.add_url_rule('/connection/follow/<user_id>',
                 'social.follow',
                 view_func=social.follow,
                 methods=METHODS_ALL)


app.add_url_rule('/connection/follow',
                 'social.follow_noid',
                  view_func=social.follow,
                  methods=METHODS_ALL,
                  defaults={'user_id': None})

app.add_url_rule('/connection/unfollow/<user_id>',
                 'social.unfollow',
                view_func=social.unfollow,
                methods=METHODS_ALL)

app.add_url_rule('/connection/unfollow',
                 'social.unfollow_noid',
                 view_func=social.unfollow,
                 methods=METHODS_ALL,
                defaults={'user_id': None})

app.add_url_rule('/visitors',
                 'visitors',
                 view_func=social.visitors,
                 methods=GET)

# Relate
app.add_url_rule('/relate/connect/<target_id>',
                 'relate.connect',
                 view_func=relate.connect,
                 methods=GET)

app.add_url_rule('/relate/create/<type>/<target_id>',
                 'relate.create',
                 view_func=relate.create,
                 methods=POST)

app.add_url_rule('/relate/delete',
                 'relate.delete',
                 view_func=relate.delete,
                 methods=GET)

app.add_url_rule('/message',
                 'message',
                 view_func=message.index,
                 methods=METHODS_ALL)

app.add_url_rule('/message/user_threads',
                 'message.user_threads',
                 view_func=message.user_threads,
                 methods=METHODS_ALL)

app.add_url_rule('/message/thread',
                 'message.thread',
                 view_func=message.thread,
                 methods=METHODS_ALL)

app.add_url_rule('/message/thread_input',
                 'message.thread_input',
                 view_func=message.thread_input,
                 methods=METHODS_ALL)

app.add_url_rule('/message/thread_header',
                 'message.thread_header',
                 view_func=message.thread_header,
                 methods=METHODS_ALL)

app.add_url_rule('/message/thread_header_images',
                 'message.thread_header_images',
                 view_func=message.thread_header_images,
                 methods=METHODS_ALL)

app.add_url_rule('/message/popupInput',
                 'message.popup_input',
                 view_func=message.popup_input,
                 methods=METHODS_ALL)

app.add_url_rule('/message/popupSubmit',
                 'message.popup_submit',
                 view_func=message.popup_submit,
                 methods=METHODS_ALL)

app.add_url_rule('/message/popupSubmitFile',
                 'message.popup_submit_file',
                 view_func=message.popup_submit_file,
                 methods=METHODS_ALL)

app.add_url_rule('/message/messagePopupImages',
                 'message.popup_image_file',
                 view_func=message.popup_image_file,
                 methods=METHODS_ALL)

app.add_url_rule('/message/submit',
                 'message.submit',
                 view_func=message.submit,
                 methods=METHODS_ALL)

app.add_url_rule('/message/submitFile',
                 'message.submit_file',
                 view_func=message.submit_file,
                 methods=METHODS_ALL)

app.add_url_rule('/message/delete_file',
                 'message.delete_file',
                 view_func=message.delete_file,
                 methods=METHODS_ALL)

app.add_url_rule('/message/popupDeleteFile',
                 'message.popup_delete_file',
                 view_func=message.popup_delete_file,
                 methods=METHODS_ALL)
'''
app.add_url_rule('/invite-friend',
                 'social.invite_friend',
                 view_func=social.invite_friend,
                 methods=METHODS_ALL)

'''
# Search
app.add_url_rule('/search',
                 'search',
                 view_func=search.main,
                 methods=METHODS_ALL)

app.add_url_rule('/search/results/<page>',
                 'search.results',
                 view_func=search.result_page,
                 methods=METHODS_ALL)

app.add_url_rule('/search/results',
                 view_func=search.result_page,
                 methods=GET,
                 defaults={'page': 0})

app.add_url_rule('/search/advanced',
                 'search.advanced',
                 view_func=search.advanced,
                 methods=METHODS_ALL)

app.add_url_rule('/opportunities',
                 'opportunities',
                 view_func=search.opportunities,
                 methods=METHODS_ALL)

# Main
app.add_url_rule('/rugby',
                 'rugby',
                 main.rugby,
                 methods=GET)

app.add_url_rule('/football',
                 'football',
                 main.football,
                 methods=GET)

app.add_url_rule('/soccer',
                 'soccer',
                 main.football,
                 methods=GET)

app.add_url_rule('/basketball',
                 'basketball',
                 main.basketball,
                 methods=GET)

# Home - Logged in
app.add_url_rule('/home',
                 'home',
                 main.home,
                 methods=GET)

app.add_url_rule('/home/<sport>',
                 'home_sport',
                 main.home_sport,
                 methods=GET)

app.add_url_rule('/main/listings',
                 'listings',
                 main.listings,
                 methods=GET)

app.add_url_rule('/main/looking-for',
                 'looking_for',
                 main.looking_for,
                 methods=GET)

app.add_url_rule('/main/suggested-profiles',
                 'suggested_profiles',
                 main.suggested_profiles,
                 methods=GET)

app.add_url_rule('/main/update',
                 'main.update',
                 main.update,
                 methods=GET)


# Payments
app.add_url_rule('/plan/pricing',
                 'plan.pricing',
                 payment.pricing,
                 methods=GET)

app.add_url_rule('/plan/checkout',
                 'plan.checkout',
                 payment.checkout_form,
                 methods=GET)

app.add_url_rule('/payment/subscribe',
                 'payment.subscribe',
                 payment.create_purchase,
                 methods=POST)

app.add_url_rule('/payment/unsubscribe',
                 'payment.unsubscribe',
                 payment.unsubscribe,
                 methods=POST)

app.add_url_rule('/settings/membership',
                 'settings.membership',
                 payment.membership,
                 methods=GET)

app.add_url_rule('/braintree/webhook',
                 'payment.webhook',
                 payment.webhook,
                 methods=POST)

# stats
app.add_url_rule('/stats',
                 'stats.index',
                 view_func=stats.index)

app.add_url_rule('/stats/csv',
                 'stats.csv',
                 view_func=stats.csv)

app.add_url_rule('/stats/users-per-hour/<string:key>',
                 'stats.usersperhour',
                 view_func=stats.usersperhour,
                 methods=GET)

app.add_url_rule('/stats/total-users-today/<string:key>',
                 'stats.totaluserstoday',
                 view_func=stats.totaluserstoday,
                 methods=GET)

app.add_url_rule('/stats/users-per-day-of-week/<string:key>',
                 'stats.users_per_day_of_week',
                 view_func=stats.users_per_day_of_week,
                 methods=GET)

app.add_url_rule('/stats/weekly-totals/<string:key>',
                 'stats.weekly_totals',
                 view_func=stats.weekly_totals,
                 methods=GET)
