import math
from flask import jsonify
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for
from flask.ext.login import login_required
from flask.ext.login import current_user
from forms.post import PostForm
from posts import controller as post_controller
from social import controller
from payment import controller as payment_controller

@login_required
def follow(user_id):
    _is_allowed = payment_controller.pro_plan(current_user.user)
    print _is_allowed
    if not _is_allowed:
        return jsonify(
            replacement_html=render_template('social/permission_denied.html', not_allowed=_is_allowed))
    user_id = request.values.get('user_id', user_id)
    if not user_id:
        abort(404)
    message_popup = request.args.get('message_popup')
    controller.add_follow(current_user.user.id, user_id)
    if not request.is_xhr:
        return redirect(url_for('profile.main', user_id=user_id))

    if message_popup:
        return render_template('profile/follow_from_popup.html',
            user=controller.get_user(user_id))
    
    return jsonify(
        status=1,
        class_to_replace='follow-button-holder-user-id-' + user_id,
        replacement_html=render_template('social/follow_replacement.html', user_id=user_id))


@login_required
def unfollow(user_id):
    _is_allowed = payment_controller.pro_plan(current_user.user)
    print _is_allowed
    if not _is_allowed:
        return jsonify(
            replacement_html=render_template('social/permission_denied.html', not_allowed=_is_allowed))
    user_id = request.values.get('user_id', user_id)
    if not user_id:
        abort(404)

    controller.remove_follow(current_user.user.id, user_id)
    if not request.is_xhr:
        return redirect(url_for('profile.main', user_id=user_id))

    return jsonify(
        status=0,
        class_to_replace='follow-button-holder-user-id-' + user_id,
        replacement_html=render_template('social/unfollow_replacement.html', user_id=user_id))


@login_required
def post():
    form = PostForm()
    if form.validate():
        controller.publish_post(current_user.user, form)
        new_form = PostForm(formdata=None)
        return render_template('post/new.html', new_post_form=new_form)

    raise UserWarning("Invalid request")


@login_required
def post_delete(id):
    controller.delete_post(current_user.user, id)
    return ''

@login_required
def post_comment():
    post_id = int(request.form.get('post'))
    text = request.form.get('text')
    if not text or not post_id:
        raise UserWarning("Invalid comment form")
    controller.save_comment(post_id, current_user.user, text) 
    return ''


@login_required
def post_list():
    user = current_user.user
    posts = post_controller.get_all_posts_for_sports(
        user,
        sports=user.sports_list,
        role=user.profile.role,
        page=int(request.form.get('page', 1)))
    return render_template('post/list.html',
        user_id=request.args.get('user_id'),
        page=request.form.get('page', 1),
        own=request.form.get('own', False),
        posts=posts)


@login_required
def favourite_post():
    post_id = int(request.args.get('post_id', 0))
    controller.favourite_post(post_id, current_user.user)
    return jsonify(
        class_to_replace='favourite-button-holder-post-id-' + str(post_id),
        replacement_html=render_template('social/favourite_replacement.html',
            post_id=post_id))


@login_required
def unfavourite_post():
    post_id = int(request.args.get('post_id', 0))
    controller.unfavourite_post(post_id, current_user.user)
    return jsonify(
        class_to_replace='favourite-button-holder-post-id-' + str(post_id),
        replacement_html=render_template('social/unfavourite_replacement.html',
            post_id=post_id))


@login_required
def connections():
    page = int(request.args.get('page', 0))
    type = request.args.get('type', 'followers')
    if type not in ['followers', 'following']:
        abort(403)

    followers = current_user.user.get_followers_count()
    following = current_user.user.get_following_count()
    if type == 'followers':
        users = controller.get_followers(current_user.user.id, page)
        pages = int(math.ceil(followers / 20.0))
    else:
        users = controller.get_following(current_user.user.id, page)
        pages = int(math.ceil(following / 20.0))

    results_url = url_for('connections', type=type, page='-page-')

    return render_template('connections/index.html',
            type=type,
            users=users,
            current_page=page,
            total_pages=pages,
            results_url=results_url)


@login_required
def visitors():
    page = int(request.args.get('page', 0))
    visitors, total_visitors = controller.get_visitors(current_user.user.id, page)
    results_url = url_for('visitors', page='-page-')
    pages = int(math.ceil(total_visitors / 20.0))

    return render_template('visitors/index.html',
            users=visitors,
            total_pages=pages,
            current_page=page,
            results_url=results_url)

