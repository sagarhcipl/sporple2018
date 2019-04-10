import boto
import db
import logging
import os.path
from config import image_sizes
from flask import abort
from flask import render_template
from flask import Response
from flask import request
from flask import send_from_directory
from flask import stream_with_context
from flask.ext.login import current_user
from flask.ext.login import login_required
from forms.image_attachment import ImageAttachmentForm
from main import app
from main import database as d
from uploads import upload


def proxy(path):
    response = _find_image(path)
    if response:
        return response

    # Give up, Return file not found.
    return send_from_directory(app.static_folder, 'images/img_not_found.png')


'''
Checks both local and remote.
'''
def _find_image(path):
    response = None
    if not app.config['S3_UPLOAD_ENABLE']:
        # First try to find a local file.
        response = _find_local(path)
    if not response:
        response = _find_remote(path)
    return response


'''
Check for s3 only
'''
def _find_remote(path):
    conn = boto.connect_s3(app.config['S3_KEY'], app.config['S3_SECRET'])
    bucket = conn.get_bucket(app.config['S3_BUCKET'], validate=False)
    key = boto.s3.key.Key(bucket)
    key.key = app.config['S3_UPLOAD_DIRECTORY'] + '/' + path
    try:
        key.open_read()
        headers = dict(key.resp.getheaders())
        response = Response(key, headers=headers, mimetype='image')
        response.cache_control.max_age = 31556926
        return response
    except boto.exception.S3ResponseError as e:
        logging.warning("S3 image not found for key %s" % key.key)
    return None


'''
Checks local disk only. Used for dev enviornment.
'''
def _find_local(path):
    file_path =  app.static_folder + '/uploads/' + path
    if os.path.isfile(file_path):
        dirpath = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        return send_from_directory(dirpath, filename)

    return None


@login_required
def attachment():
    user_id = request.args.get('user_id')
    profile = db.UserProfile.query.get(user_id)
    if not profile:
        abort(403)
    if profile.user_id != current_user.user.id \
        and profile.managed_by_id != current_user.user.id:
        abort(403)
    form = ImageAttachmentForm()
    if form.filename.data:
        profile_upload_dir = 'ooipAttachments/sfGuardUserProfile/default'
        filename = upload.s3_upload(form.filename.data,
            sub_dir='/' + profile_upload_dir)
        file_path = '/uploads/' + profile_upload_dir + '/' + filename
        resize_path = image_sizes.get_resized(file_path, 'thumb')
        upload.s3_resize(file_path, resize_path, 'thumb')

        original_file = os.path.splitext(filename)
        attachment = db.Attachment(
                author_id = profile.user_id,
                attachable_id = profile.user_id,
                attachable_model = 'sfGuardUserProfile',
                filename = original_file[0],
                folder = profile_upload_dir,
                fileextension = original_file[1][1:],
                attachment_namespace = 'default')
        d.session.add(attachment)
        d.session.commit()

    return 'success'

@login_required
def delete_attachment(attachment_id):
    attachment = db.Attachment.query.get(int(attachment_id))
    if attachment.author_id != current_user.user.id:
        raise UserWarning("Invalid command")
    d.session.delete(attachment)
    d.session.commit()
    return 'Deleted'
