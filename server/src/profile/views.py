import random
from flask import abort
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask.ext.login import current_user
from flask.ext.login import login_required
from forms import query_selectors
from forms.achievement import AchievementForm
from forms.application import ApplicationForm
from forms.basic_athlete_information import BasicAthleteInformationForm
from forms.basic_agent_information import BasicAgentInformationForm
from forms.basic_club_information import BasicClubInformationForm
from forms.career_summary import CareerSummaryForm
from forms.personal_statement import PersonalStatementForm
from forms.career_item import CareerItemForm
from forms.client import ClientForm
from forms.club_about import ClubAboutForm
from forms.endorsement import EndorsementForm
from forms.image_attachment import ImageAttachmentForm
from forms.profile_image import ProfileImageForm
from forms.listing import ListingForm
from forms.looking_for import LookingForForm
from forms.player_media_reel import PlayerMediaReelForm
from forms.qualification import QualificationForm
from forms.twitter import TwitterForm
from main import app
from main import database as d
from auth import controller as acontroller
from profile import controller as pcontroller
from relate import controller as rcontroller
from listing import controller as lcontroller
from payment import controller as payment_controller
import db

''' Clear a profile field '''
@login_required
def clear_field(path):
    profile = current_user.user.profile
    pcontroller.clear_field(profile, request.values.get('db_field_name'))
    return ''


def main(user_id):
    try:
        profile = pcontroller.get_profile_from_user_id(user_id)
        print profile.sport
    except UserWarning:
        abort(404)

    if not profile.role or not profile.user.is_active:
        abort(404)
    return redirect(url_for('profile.slug', slug=profile.slug), code=301)


def slug(slug):
    try:
        profile, slug2 = pcontroller.get_profile_from_slug(slug)
    except UserWarning:
        abort(404)
    if slug != slug2:
        return redirect(url_for('profile.slug', slug=slug2), code=301)
    if not profile.sport:
        abort(404)
    return sport_slug(profile.sport.slug, profile.slug)


def sport_slug(sport, slug):
    try:
        profile, slug2 = pcontroller.get_profile_from_slug(slug)
    except UserWarning:
        abort(404)

    if not profile.sport:
        abort(404)

    if profile.user.sport.slug != sport or slug != slug2:
        code = 301 if slug != slug2 else 302
        return redirect(url_for('profile.sport_slug',
            sport=profile.sport.slug, slug=slug2), code=code)

    # 07/26: Hard-coding to block a profile. This will ensure if the user
    # is already logged in then he will be logged out at this point.
    # Also adding this check in auth/views to ensure he cannot log back in.
    # Discuss with Mat to remove this after a couple of months.
    if profile.user_id == 4892:
        # Also if this is user's own profile, sign him out.
        if current_user.is_authenticated and current_user.user.id == 4892:
            return redirect(url_for('logout'))
        abort(404)

    if current_user.is_authenticated:
        pcontroller.update_user_visit(profile.user_id, current_user.user.id)

    seed = random.randint(1, 100)
    is_owner = _is_owner(profile)
    role_slug = profile.role.slug
    params = {
        'profile': profile,
        'endorsements': pcontroller.get_endorsements(profile),
        'qualifications': pcontroller.get_qualifications(profile),
        'related_profiles': pcontroller.get_related_profiles(profile, seed=seed),
        'clients': pcontroller.get_clients(profile),
        'posts': pcontroller.get_posts_for_user(profile.user_id),
        'title': (profile.user.sport.name + ' | '
            + profile.fullname + ' | '
            + app.config['BASE_NAME']),
        'is_owner': is_owner,
        'gallery_images': profile.get_attachments(),
        'twitter_form': TwitterForm(obj=profile),
        'seed': seed,
        'is_following': (current_user.is_authenticated
            and (current_user.user.is_following(profile.user_id))),
        'target_role': role_slug,
    }
    if current_user.is_authenticated:
        params['user_role'] = current_user.user.role_slug
        params['is_allow_to_chat'] = profile.is_allowed_to_message

    if is_owner:
        params['image_form'] = ImageAttachmentForm() # For gallery
        params['profile_image_form'] = ProfileImageForm() # For profile photo

    if role_slug == 'agent':
        params['looking_for_list'] = pcontroller.get_looking_for_list(profile)
    elif role_slug == 'club':
        params['listings'] = lcontroller.get_listings_for_club(profile.user_id)
        params['club_stars'] = rcontroller.get_legends(profile),
        params['current_team'] = pcontroller.get_current_team(profile)
        params['past_team'] = pcontroller.get_past_team(profile)
    elif role_slug == 'athlete':
        params['career_items'] = pcontroller.get_career_items(profile)
        params['team'] = pcontroller.get_team(profile)
        params['achievements'] = pcontroller.get_achievements_chronologically(profile)
    return render_template('profile/index_' + role_slug + '.html', **params)


def related_profiles():
    user_id = request.args.get('user_id')
    page = request.args.get('page')
    seed = request.args.get('seed')
    if not seed:
        seed = random.randint(1, 100)
    if not user_id:
        abort(403)

    params = {
        'page': page,
        'seed': seed,
        'profiles': pcontroller.get_related_profiles(user_id, page, seed)
    }
    return render_template('profile/related_profiles.html', **params)


@login_required
def upload_profile_photo():
    try:
        profile = _get_owner_profile()
        form = ProfileImageForm()
        if request.method == 'POST' and form.validate():
            pcontroller.upload_photo(profile, form)
            return 'success'
    except Exception as e:
        return str(e)

    return ''

@login_required
def edit_basic_athlete():
    profile = _get_owner_profile()
    form = BasicAthleteInformationForm(obj=profile)
    form.user_position_list.query = query_selectors.user_position_list(profile.sport.id, blank=True)
    if request.method == 'POST' and form.validate():
        old_browser_mode = request.form.get('oldBrowserMode')
        pcontroller.update_athlete_profile(profile, form)
        if old_browser_mode:
            return profile.image

        if request.is_xhr:
            return 'success'
        else:
            return redirect(url_for('profile.slug', slug=profile.slug))
    elif request.method == 'GET':
        form.set_form_data(profile)
    return render_template('forms/basic_athlete_info.html', form=form, profile=profile)


@login_required
def edit_basic_agent():
    profile = current_user.user.profile
    form = BasicAgentInformationForm(obj=profile)
    form.user_sport.query = query_selectors.sport_list(blank=True)
    if request.method == 'POST' and form.validate():
        old_browser_mode = request.form.get('oldBrowserMode')
        pcontroller.update_agent_profile(profile, form)
        if old_browser_mode:
            return profile.image

        if request.is_xhr:
            return 'success'
        else:
            return redirect(url_for('profile.slug', slug=profile.slug))
    elif request.method == 'GET':
        form.set_form_data(profile)
    return render_template('forms/basic_agent_info.html', form=form, profile=profile)


@login_required
def edit_basic_club():
    profile = current_user.user.profile
    form = BasicClubInformationForm(obj=profile)
    if request.method == 'POST' and form.validate():
        old_browser_mode = request.form.get('oldBrowserMode')
        pcontroller.update_club_profile(profile, form)
        if old_browser_mode:
            return profile.image
        
        if request.is_xhr:
            return 'success'
        else:
            return redirect(url_for('profile.slug', slug=profile.slug))
    return render_template('forms/basic_club_info.html', form=form, profile=profile)


@login_required
def view_player_media():
    profile = _get_owner_profile()
    return render_template('profile/media.html',
        profile=profile,
        is_owner=True)


@login_required
def player_media():
    profile = _get_owner_profile()
    form = PlayerMediaReelForm()
    if request.method == 'POST' and form.validate():
        try:
            pcontroller.save_player_media(profile, form)
            return render_template('profile/media.html',
                    profile=profile, is_owner=True)
        except UserWarning,e:
            form.reel_image.errors.append(e.message)

    referrer = url_for('profile.main', user_id=profile.user_id)
    image_form = ImageAttachmentForm(referrer=referrer)
    attachments = profile.get_attachments()
    return render_template('forms/media.html',
        profile=profile,
        edit=True,
        nr_attachments=len(attachments),
        attachments=attachments,
        form=form,
        image_form=image_form)


@login_required
def can_apply(listing_id, role):
    profile = current_user.user.profile
    if role == 'club':
        listing = pcontroller.get_listing(int(listing_id))
    else:
        listing = pcontroller.get_looking_for(int(listing_id))
    missing = {}
    if not profile.address_country_id:
        missing['country'] = 'Country of Residence'
    if not profile.nationality_id:
        missing['nationality'] = 'Nationality'
    if not profile.reel_video_url:
        missing['reel_video'] = 'Player Showreel video'
    if not profile.birthday:
        missing['birthday'] = 'Date of Birth'
    if not profile.height:
        missing['height'] = 'Height'
    if not profile.weight:
        missing['weight'] = 'Weight'
    if not profile.user.career_items:
        missing['career_info'] = 'Career Timeline'

    if not missing:
        if lcontroller.is_eligible(profile, listing):
            return 'success'
        else:
            return render_template('profile/not_eligible.html')

    complete_percent = 100 - (len(missing)*5)
    return render_template('profile/incomplete_profile.html',
            missing=missing, complete=complete_percent)


@login_required
def player_media_thumb():
    profile = current_user.user.profile
    attachments = profile.get_attachments()
    image_form = ImageAttachmentForm()
    return render_template('profile/thumb_list.html',
        profile=profile,
        edit=True,
        nr_attachments=len(attachments),
        attachments=attachments,
        image_form=image_form)

@login_required
def personal_statement(user_id):
    profile = pcontroller.get_profile_from_user_id(user_id)
    return render_template('profile/personal_statement.html', profile=profile)


@login_required
def edit_personal_statement():
    profile = _get_owner_profile()
    form = PersonalStatementForm(request.form, obj=profile)
    if request.method == 'POST' and form.validate():
        profile.personal_statement = form.personal_statement.data
        d.session.commit()
        return 'success'
    else:
        return render_template('forms/personal_statement.html', form=form, profile=profile)


@login_required
def career_summary(user_id):
    profile = pcontroller.get_profile_from_user_id(user_id)
    return render_template('profile/career_summary.html', profile=profile)

@login_required
def edit_career_summary():
    profile = _get_owner_profile()
    form = CareerSummaryForm(request.form, obj=profile)
    if request.method == 'POST' and form.validate():
        profile.career_summary = form.career_summary.data
        d.session.commit()
        return 'success'
    else:
        return render_template('forms/career_summary.html', form=form, profile=profile)


@login_required
def edit_career_item(id):
    profile = _get_owner_profile()
    career_item = None

    if id:
        career_item = pcontroller.get_career_item(id)
    form = CareerItemForm(obj=career_item)

    if id:
        form.set_form_data(career_item)
    if request.method == 'POST' and form.validate():
        pcontroller.save_career_item(form, career_item, profile)
        career_items = pcontroller.get_career_items(profile)
        return 'success'

    else:
        return render_template('forms/career_item.html', form=form, career_item_id=id, profile=profile)


@login_required
def delete_career_item(id):
    career_item = pcontroller.get_career_item(id)
    pcontroller.delete_career_item(current_user.user, career_item)
    return ''

@login_required
def edit_achievement(id):
    profile = _get_owner_profile()

    achievement = None
    if id:
        achievement = pcontroller.get_achievement(id)
    form = AchievementForm(request.form, achievement)

    if request.method == 'POST' and form.validate():
        pcontroller.save_achievement(form, achievement, profile)
        achievements = pcontroller.get_achievements_chronologically(profile)
        return 'success'
    else:
        return render_template('forms/achievement.html', form=form, achievement_id=id, profile=profile)


@login_required
def delete_achievement(id):
    try:
        achievement = pcontroller.get_achievement(id)
    except UserWarning:
        return ''
    pcontroller.delete_achievement(current_user.user, achievement)
    return ''



@login_required
def edit_endorsement(id):
    profile = _get_owner_profile()
    endorsement = None

    if id:
        endorsement = pcontroller.get_endorsement(id)
    form = EndorsementForm(request.form, endorsement)
    if id:
        form.set_form_data(endorsement)

    if request.method == 'POST' and form.validate():
        pcontroller.save_endorsement(form, endorsement, profile)
        endorsements = pcontroller.get_endorsements(profile)
        return 'success'
    else:
        return render_template('forms/endorsement.html', form=form, endorsement_id=id, profile=profile)


@login_required
def delete_endorsement(id):
    try:
        endorsement = pcontroller.get_endorsement(id)
    except UserWarning:
        return ''
    pcontroller.delete_endorsement(current_user.user, endorsement)
    return ''

@login_required
def edit_qualification(id):
    profile = current_user.user.profile
    qualification = None
    
    if id:
        qualification = pcontroller.get_qualification(id)
    form = QualificationForm(request.form, qualification)

    if request.method == 'POST' and form.validate():
        pcontroller.save_qualification(form, qualification, profile)
        qualifications = pcontroller.get_qualifications(profile)
        return 'success'
    else:
        return render_template('forms/qualification.html', form=form, qualification_id=id)


@login_required
def delete_qualification(id):
    qualification = pcontroller.get_qualification(id)
    pcontroller.delete_qualification(current_user.user, qualification)
    return ''

@login_required
def edit_club_about():
    profile = current_user.user.profile 
    form = ClubAboutForm(obj=profile)
    if request.method == 'POST' and form.validate():
        profile.career_summary = form.career_summary.data
        d.session.commit()
        return 'success'
    else:
        return render_template('forms/club_about.html', profile=profile, form=form)


@login_required
def clients():
    profile = current_user.user.profile
    user_clients = pcontroller.get_clients(profile)
    return render_template('agent/clients.html', clients=user_clients,
            profile=profile, hide_title=True, is_owner=True)


@login_required
def edit_client(id):
    profile = current_user.user.profile
    client = None

    if id:
        client = pcontroller.get_client(id)
    form = ClientForm(obj=client)
    form.position.query = query_selectors.user_position_list(profile.user.sport.id)

    if request.method == 'POST':
        user_agent = request.headers.get('User-Agent')
        client_profile = acontroller.save_client(form, profile, user_agent)
        return render_template('agent/client_success.html', profile=client_profile)
    else:
        return render_template('forms/client.html', form=form, client_id=id, client=client)


@login_required
def delete_client(id):
    try:
        client = pcontroller.get_client(id)
    except UserWarning:
        return jsonify(errors=[])
    pcontroller.delete_client(current_user.user, client)
    return jsonify(errors=[])


@login_required
def edit_looking_for(id):
    subscription = payment_controller._subscription_object(current_user.user)
    profile = current_user.user.profile
    looking_for = None
    if id:
        looking_for = pcontroller.get_looking_for(id)
    form = LookingForForm(obj=looking_for)
    form.position.query = query_selectors.user_position_list(profile.user.sport.id)
    form.country_groups.query = query_selectors.country_group_list(blank=True)

    if request.method == 'POST' and form.validate():
        pcontroller.save_looking_for(form, looking_for, profile)
        return 'success'
    else:
        return render_template('forms/looking_for.html',
                profile=profile, form=form, looking_for_id=id, premium=subscription)


@login_required
def delete_looking_for(id):
    profile = current_user.user.profile
    looking_for = pcontroller.get_looking_for(id)
    pcontroller.delete_looking_for(current_user.user, looking_for)
    return jsonify(errors=[])


def looking_for_list():
    profile = _get_profile_or_404()
    looking_for_list = pcontroller.get_looking_for_list(profile)
    return render_template('lookingfor/item.html',
            profile=profile, looking_fors=looking_for_list)


def show_looking_for():
    if not current_user.is_authenticated:
        return render_template('cannot_access.html')
    profile = _get_profile_or_404()
    looking_for_id = request.args.get('listing_id', 0)
    looking_for = pcontroller.get_looking_for(looking_for_id)
    is_owner = current_user.is_authenticated and \
            current_user.user.id == looking_for.user_id
    return render_template('lookingfor/show.html',
            profile=profile, looking_for=looking_for, is_owner=is_owner)


@login_required
def edit_club_listing():
    profile = current_user.user.profile
    listing = None

    id = request.args.get('listing_id', 0)
    if id:
        listing = pcontroller.get_listing(int(id))
    form = ListingForm(obj=listing)
    form.position.query = query_selectors.user_position_list(profile.sport.id)
    form.country_groups.query = query_selectors.country_group_list(blank=True)
    if request.method == 'POST' and form.validate():
        pcontroller.save_listing(form, listing, profile)
        return 'success'

    elif request.method == 'GET':
        form.set_form_data(listing)

    return render_template('forms/listing.html',
                profile=profile, listing_id=id, form=form, premium=current_user.user.is_premium())



@login_required
def delete_listing(id):
    profile = current_user.user.profile
    listing = pcontroller.get_listing(id)
    if request.method == 'POST':
        close_reason = request.form.get('close_reason')
        hired_user_id = request.form.get('delete-listing-user-id')
        athlete_name = request.form.get('outside_athlete_name')
        athlete_email = request.form.get('outside_athlete_email')
        pcontroller.delete_listing(current_user.user, listing,
            close_reason, hired_user_id,
            athlete_name, athlete_email)
        return 'success'
    else:
        return render_template('forms/delete_listings.html', listing=listing)


@login_required
def new_application():
    # import pdb
    # pdb.set_trace()
    profile = current_user.user.profile
    listing_id = request.args.get('listing_id', 0)
    role = request.args.get('role', 0)
    if role == 'club':
        listing = pcontroller.get_listing(listing_id)
    else:
        listing = pcontroller.get_looking_for(listing_id)
    if profile.role.slug != 'athlete' or not listing:
        raise UserWarning("Invalid application")

    form = ApplicationForm()
    error = ''
    if request.method == 'POST' and form.validate():
        print role
        try:
            pcontroller.save_application(form, listing, profile, role)
            return 'success'
        except UserWarning as e:
            error = e.message

    return render_template('forms/apply.html', form=form, listing=listing, error=error)


@login_required
def twitter_account():
    profile = _get_owner_profile()
    form = TwitterForm(request.form)
    if request.method == 'POST' and form.validate():
        profile.twitter_account = form.twitter_account.data
        d.session.commit()
        return render_template('profile/show_twitter_account.html', profile=profile, is_owner=True)
    return render_template('profile/edit_twitter_account.html', twitter_form=form, profile=profile)


def _is_owner(profile):
    return current_user.is_authenticated \
        and (current_user.user.id == profile.user_id \
            or current_user.user.id == profile.managed_by_id)


def _get_owner_profile():
    user_id = request.args.get('user_id')
    profile = current_user.user.profile
    if user_id:
        try:
            profile = pcontroller.get_profile_by_user_id(user_id)
        except UserWarning:
            abort(403)

    if not _is_owner(profile):
        abort(403)
    return profile


def _get_profile_or_404(user_id=None):
    user_id = request.values.get('user_id', user_id)
    if not user_id and current_user.is_authenticated:
        profile = current_user.user.profile
    else:
        try:
            profile = pcontroller.get_profile_by_user_id(user_id)
        except UserWarning:
            abort(404)

    return profile

@login_required
def get_applicant_list():
    listing_id = request.args.get('listing_id', 0)
    role = request.args.get('role', 0)
    listing = pcontroller.get_listing_from_role(listing_id, role)
    if role == 'club':
        if current_user.user.profile == listing.club.profile:
            applicants = db.Application.query.filter(db.Application.listing_id == int(listing_id)).all()
        else:
            raise UserWarning("You have no access to this")
    else:
        if current_user.user.profile == listing.user.profile:
            applicants = db.Application.query.filter(db.Application.looking_for_id == int(listing_id)).all()
        else:
            raise UserWarning("You have no access to this")

    return render_template('profile/get_applicant_list.html', applicants=applicants)