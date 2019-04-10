from flask import abort
from flask import render_template
from flask import request

from flask.ext.login import login_required
from flask.ext.login import current_user
from main import sentry
from profile import controller as pcontroller
from social import controller as scontroller
from relate import config
from relate import controller
from payment import controller as payment_controller

@login_required
def connect(target_id):
    # Current user connecting to target id.
    # Show custom message depending on roles.
    target_profile = pcontroller.get_profile_by_user_id(target_id)
    target_role_slug = target_profile.role.slug
    user_role_slug = current_user.user.role_slug

    return render_template('relate/popup_connect.html',
        target_user=target_profile.user,
        target_role=target_role_slug,
        user_role=user_role_slug)


@login_required
def create(type, target_id):
    _is_allowed = payment_controller.pro_plan(current_user.user)
    if not _is_allowed:
        return '<strong>Access Denied:</strong> You should signup premium'
    if not _is_valid_relation(type):
        sentry.captureMessage("Invalid relation:" + type)
        abort(403)
    target_profile = pcontroller.get_profile_by_user_id(target_id)
    target_user = target_profile.user
    year_start = int(request.args.get('year_start', 0))
    year_end = int(request.args.get('year_end', 0))
    club_name = request.args.get('club_name', '')
    career_item_id = int(request.args.get('career_item_id', 0))

    scontroller.add_follow(current_user.user.id, target_user.id, notify=False)
    controller.set_relation(
            current_user.user, target_user,
            year_start, year_end,
            club_name=club_name,
            type=type)

    return '<strong>Great!</strong> You are now connected to ' + target_user.name


@login_required
def delete():
    target_id = int(request.args.get('target_id', 0))
    user_id = int(request.args.get('user_id', 0))
    user = pcontroller.get_profile_by_user_id(user_id)
    if current_user.user.id not in [user.user_id, user.managed_by_id]:
        target_user = pcontroller.get_profile_by_user_id(target_id)
        if current_user.user.id not in [target_user.user_id, target_user.managed_by_id]:
            abort(403)

    controller.delete_relation(user_id, target_id)
    return ''


def _is_valid_relation(type):
    return type in config.get_all()

