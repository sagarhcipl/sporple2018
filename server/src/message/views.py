from flask import jsonify
from flask import render_template
from flask import request
from flask import session
from flask.ext.login import current_user
from flask.ext.login import login_required
from main import sentry
from message import controller
from uploads import upload
from profile import controller as pcontroller


@login_required
def index():
    return render_template('message/index.html', hide_footer=True)


@login_required
def user_threads():
    filter = request.form.get('filter')
    page = int(request.args.get('page', 0))
    threads = controller.get_thread_users_for(current_user.user, filter, page)
    return render_template('message/user_threads.html', threads=threads)


@login_required
def thread():
    thread_id = int(request.args.get('thread_id'))
    messages = controller.get_messages(thread_id)
    controller.messages_read(current_user.user, thread_id)
    return render_template('message/thread.html', messages=messages)


@login_required
def thread_input():
    thread_id = int(request.args.get('thread_id'))
    return render_template('message/thread_input.html', thread_id=thread_id)


@login_required
def thread_header():
    thread_id = int(request.args.get('thread_id'))
    other_users = controller.get_message_users_for_thread(
            thread_id, current_user.user)
    return render_template('message/thread_header.html',
        other_users=other_users)


@login_required
def thread_header_images():
    thread_id = int(request.args.get('thread_id'))
    image = session.get('message_uploads_thread_%d' % thread_id)
    icon = _file_icon(image)
    return render_template('message/thread_header_images.html',
            image=image, icon=icon)


@login_required
def delete_file():
    thread_id = int(request.form.get('thread_id'))
    # Remove old file
    # Remove user attribute
    session.pop('message_uploads_thread_%d' % thread_id, None)
    return ''


@login_required
def popup_input():
    target_user_id = int(request.args.get('target_user_id'))
    target_user = controller.get_user(target_user_id)
    profile = pcontroller.get_profile_from_user_id(target_user_id)
    # if current_user.user.has_msg_limit_reached():
    #     sentry.captureMessage("Message_limit_reached", extra={'target_user_id': target_user_id})
    #     return render_template('message/limit_reached.html', target_user=target_user)
    if current_user.user.role_slug == 'athlete':
        message_allow = profile.is_allowed_to_message
        print message_allow
    else:
        message_allow = True
    # Show premium account subscription for agents and clubs.
    if not current_user.user.can_send_message():
       return render_template('plan/show_premium_popup.html', target_user=target_user)
    else:
        return render_template('message/popup_input.html', target_user=target_user, message_allow=message_allow)


@login_required
def submit():
    if not current_user.user.role_slug == 'athlete' and not current_user.user.is_premium():
        return jsonify(success=False, error="Please subscribe to premium membership")
    thread_id = int(request.form.get('thread_id'))
    thread = controller.get_thread(thread_id)
    body = request.form.get('body')
    session_uploads_var = session.get('message_uploads_thread_%d' % thread_id)
    if not _has_sports_bridge(body):
        try:
            controller.save_message_thread(current_user.user, thread, body,
                session_uploads_var)
        except UserWarning as e:
            return jsonify(success=False, error=e.message)
    if session_uploads_var:
        session.pop('message_uploads_thread_%d' % thread_id, None)
    return jsonify(success=True)


@login_required
def submit_file():
    thread_id = int(request.form.get('thread_id'))
    file = request.files.get('message-file')
    if not file or not thread_id:
        raise UserWarning("Invalid request")
    filename = upload.s3_upload(file, sub_dir='/message')
    session['message_uploads_thread_%d' % thread_id] = 'message/' + filename
    return ''


@login_required
def popup_submit():
    target_user_id = int(request.form.get('target_user_id'))
    target_user = controller.get_user(target_user_id)
    body = request.form.get('body')
    session_uploads_var = session.get('message_uploads_user_%d' % target_user_id)
    if current_user.user.id == target_user_id:
        raise UserWarning("Cannot start a thread with yourself")
    if not _has_sports_bridge(body):
        try:
            controller.save_message_user(
                current_user.user, target_user, body,
                session_uploads_var)
        except UserWarning as e:
            return render_template('message/popup_input.html', target_user=target_user,
                body=body, error=e.message)
    if session_uploads_var:
        session.pop('message_uploads_user_%d' % target_user_id, None)
    return render_template('message/popup_submit.html', target_user=target_user)


@login_required
def popup_delete_file():
    target_user_id = int(request.form.get('target_user_id'))
    session.pop('message_uploads_user_%d' % target_user_id, None)
    return ''

@login_required
def popup_submit_file():
    target_user_id = int(request.form.get('target_user_id'))
    file = request.files.get('message-file')
    if not file or not target_user_id:
        return 'x'
    filename = upload.s3_upload(file, sub_dir='/message')
    session['message_uploads_user_%d' % target_user_id] = 'message/' + filename
    return ''

@login_required
def popup_image_file():
    target_user_id = int(request.args.get('target_user_id'))
    image = session.get('message_uploads_user_%d' % target_user_id)
    icon = _file_icon(image)
    return render_template('message/popup_images.html',
            image=image, icon=icon)


def _file_icon(file_path):
    if not file_path:
        return ''
    file_map = {
        'jpeg' : '/uploads/' + file_path,
        'jpg'  : '/uploads/' + file_path,
        'gif'  : '/uploads/' + file_path,
        'png'  : '/uploads/' + file_path,
        'doc'  : '/static/images/word-icon.jpg',
        'docx' : '/static/images/word-icon.jpg',
        'xls'  : '/static/images/excel-icon.png',
        'xlsx' : '/static/images/excel-icon.png',
        'pdf'  : '/static/images/pdf-icon.png',
    }
    extension = file_path.split(".")[-1]
    return file_map.get(extension, '')


def _has_sports_bridge(text):
    result = 'sportsbridge' in text.lower()
    if result:
        sentry.captureMessage("[SportsBridge] Message flagged", extra={'message': text})
    return result
