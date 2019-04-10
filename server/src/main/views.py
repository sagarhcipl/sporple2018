import datetime
import random
import util

from agent import controller as acontroller
from flask import jsonify
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for
from flask.ext.login import current_user
from flask.ext.login import login_required
from forms.post import PostForm
from listing import controller as lcontroller
from looking_for import controller as lfcontroller
from main import app
from posts import controller as post_controller
from profile import controller as pcontroller



def index():
    # If user is authenticated, send them to the real home page.
    if current_user.is_authenticated:
        sport = request.args.get('sport','')
        if not sport:
            sport = current_user.user.sport_slug
        return redirect(url_for('home_sport', sport=sport))

    params = {}
    params['featured_profiles'] = pcontroller.get_featured_profiles(0)
    params['latest_listings'] = lcontroller.get_latest_listing('rugby')
    params['total_users'] = pcontroller.get_total_users()
    meta = {
        'og:title': app.config['BASE_TITLE'],
        'og:site_name': app.config['BASE_NAME'],
        'og:url': app.config['BASE_URL'],
        'og:description': 'Connecting athletes agents & clubs across the globe',
        'og:image': url_base('images/facebook-image-dotcom.jpg')
    }
    params['meta'] = meta
    params['show_olark'] = True
    params['header_type'] = 'absolute-header'
    params['exp'] = random.randint(1,3)
    return render_template('main/index.html', **params)


def rugby():
    if current_user.is_authenticated:
        sport = current_user.user.sport_slug or 'rugby'
        return redirect(url_for('home_sport', sport=sport))

    return redirect('/')
    params = {}
    params['featured_profiles'] = pcontroller.get_featured_profiles(4)
    params['latest_listings'] = lcontroller.get_latest_listing('rugby')
    meta = {
        'og:title': 'Sporple | Your Global Rugby Network',
        'og:site_name': app.config['BASE_NAME'],
        'og:url': url_base('rugby'),
        'og:description': 'Connecting athletes agents & clubs across the globe',
        'og:image': url_base('images/fb_rugby.jpg')
    }
    params['meta'] = meta
    params['show_olark'] = True
    params['header_type'] = 'absolute-header'
    return render_template('main/index_rugby.html', **params)


def football():
    if current_user.is_authenticated:
        sport = current_user.user.sport_slug or 'football'
        return redirect(url_for('home_sport', sport=sport))

    return redirect('/')
    params = {}
    meta = {
        'og:title': 'Sporple | Your Global Football Network',
        'og:site_name': app.config['BASE_NAME'],
        'og:url': url_base('football'),
        'og:description': 'Connecting athletes agents & clubs across the globe',
        'og:image': url_base('images/facebook-image-dotcom.jpg')
    }
    params['meta'] = meta
    params['show_olark'] = True
    return render_template('main/index_football.html', **params)


def basketball():
    if current_user.is_authenticated:
        sport = current_user.user.sport_slug or 'basketlball'
        return redirect(url_for('home_sport', sport=sport))

    return redirect('/')
    params = {}
    params['featured_profiles'] = pcontroller.get_featured_profiles(4)
    params['latest_listings'] = lcontroller.get_latest_listing('basketball')
    meta = {
        'og:title': 'Sporple | Your Global Basketball Network',
        'og:site_name': app.config['BASE_NAME'],
        'og:url': url_base('basketball'),
        'og:description': 'Connecting athletes agents & clubs across the globe',
        'og:image': url_base('images/facebook-image-dotcom.jpg')
    }
    params['meta'] = meta
    params['show_olark'] = True
    params['header_type'] = 'absolute-header'
    return render_template('main/index_basketball.html', **params)


@login_required
def home():
    sport = request.args.get('sport','')
    if not sport:
        sport = current_user.user.sport_slug
    return redirect(url_for('home_sport', sport=sport))


@login_required
def home_sport(sport=None):
    if not sport:
        sport = current_user.user.sport_slug

    page = request.values.get('page', 1)
    sports = current_user.user.sports_list

    params = {
        'sport': sport,
        'show_olark': True,
        'nr_following': current_user.user.get_following_count(),
        'nr_followers': current_user.user.get_followers_count(),
        'posts': post_controller.get_all_posts_for_sports(
            current_user.user, sports, current_user.user.profile.role, page),
        'new_post_form': PostForm(),
        'listings': lcontroller.get_listings_for_sports(sports, 1),
        'looking_for_list': lfcontroller.get_looking_for_by_sports(sports, 1),
        'suggested_profiles': pcontroller.get_suggested_profiles(
            current_user.user.sport.id, page=1),
        'page': 1,
    }
    return render_template('main/home_sport.html', **params)


@login_required
def listings():
    page = int(request.args.get('page', 1))
    sport_id = current_user.user.profile.sport_id
    params = {
        'listing': lcontroller.get_listing_for_sport(sport_id, page),
    }
    return render_template('main/listing.html', **params)


@login_required
def looking_for():
    page = int(request.args.get('page', 1))
    sport_id = current_user.user.profile.sport_id
    params = {
        'looking_for': acontroller.get_looking_for(sport_id, page),
    }
    return render_template('main/looking_for.html', **params)


@login_required
def suggested_profiles():
    page = int(request.args.get('page', 1))
    sport_id = current_user.user.sport.id
    role_id = current_user.user.profile.role_id

    params = {
        'suggested_profiles': pcontroller.get_suggested_profiles(sport_id, page)
    }
    return render_template('main/suggested_profiles.html', **params)


def favicon():
    return send_from_directory(app.static_folder, 'images/favicon.ico')


def robots_txt():
    response = make_response(render_template('robots.txt'))
    response.headers['Content-type'] = 'text/plain; charset=utf-8'
    return response


def update():
    params = {}
    user = {'is_authenticated': current_user.is_authenticated}
    if current_user.is_authenticated:
        user['id'] = current_user.user.id
        params['message'] = {
            'nb_unread_messages': current_user.user.get_unread_messages()
        }
        params['missing_profile_pic'] = not current_user.user.profile.image

    params['user'] = user
    return jsonify(**params)


def url_base(string):
    return app.config['BASE_URL'] + string
