import braintree
from config import plan
from flask import abort
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import Response
from flask import request
from flask import url_for
from flask.ext.login import current_user
from flask.ext.login import login_required
from main import app
from main import sentry
from payment import controller
import pdb
import db


def pricing():
    role_slug = ''

    if not current_user.user.plan == 'intro':
        abort(403)

    if current_user.is_authenticated:
        role_slug = current_user.user.role_slug
        print role_slug
    return render_template('plan/details.html', role_slug=role_slug)


@login_required
def checkout_form():
    if current_user.user.role_slug == 'athlete':
        return redirect(url_for('home'))
    plan = controller._subscription_object(current_user.user)
    client_token = braintree.ClientToken.generate()
    return render_template('plan/checkout_form.html', client_token=client_token, plan=plan)


@login_required
def create_purchase():
    nonce = request.form.get('payment_method_nonce', '')
    if not nonce:
        abort(403)

    plan_type = request.form.get('plan_type', 'intro')
    user_role_slug = current_user.user.profile.role.slug
    plan_length = request.form.get('plan_length', 'monthly')
    plan_info = None

    if plan_length not in ['monthly', 'annual']:
        raise UserWarning("Invalid plan length selected: " + plan_length)

    plan_info = plan.get(user_role_slug, plan_type)
    if not plan_info:
        abort(403)

    result = controller.create_subscription(
            current_user.user,
            nonce,
            user_role_slug,
            plan_type,
            plan_length)

    if result.is_success:
        return render_template('plan/success.html')
    else:
        sentry.captureMessage("Transaction failed: " + result.message,
            extra=result.params)
        return result.message

@login_required
def membership():
    subscription = None
    if current_user.user.plan == 'pro':
        subscription = controller.get_subscription(current_user.user)
    plan_info = plan.get(current_user.user.role_slug, current_user.user.plan)

    return render_template('settings/membership.html',
        subscription = subscription, plan_info=plan_info)


@login_required
def unsubscribe():
    if current_user.user.plan == 'intro':
        return jsonify(success=True)
    result = controller.deactivate_subscription(current_user.user)
    if not result or result.is_success:
        return jsonify(success=True)
    return jsonify(error=result.message)


def webhook():
    webhook_notification = braintree.WebhookNotification.parse(
        str(request.form['bt_signature']), request.form['bt_payload'])
    if webhook_notification.kind == 'subscription_charged_successfully':
        controller.recurring_subscription(webhook_notification)

    if webhook_notification.kind == 'subscription_went_past_due':
        controller.subscription_due(webhook_notification.subscription.id)

    sentry.captureMessage('Subscription Error:' + webhook_notification.kind,
        extra={'subscription_id': webhook_notification.subscription.id})
    return Response(status=200)

