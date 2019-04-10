import braintree
import datetime
import db
from config import plan
from etasks import emails
from main import database as d
from main import sentry


def create_subscription(user, nonce, role_slug, plan_type, plan_length):
    subscription_obj = _subscription_object(user)
    if subscription_obj:
        cancel = braintree.Subscription.cancel(subscription_obj.braintree_subscription_id)
        if subscription_obj.status == 'active':
            subscription_obj.status = 'end'
            d.session.commit()
    result = braintree.Customer.create({
        'first_name': user.profile.firstname,
        'last_name': user.profile.lastname,
        'email': user.username,
        'payment_method_nonce': nonce,
    })

    if not result.is_success or not result.customer.payment_methods:
        return result

    subscription = db.UserSubscription(
        user_id=user.id,
        plan_type=plan_type,
        plan_length=plan_length,
        braintree_customer_id=result.customer.id,
        payment_method_token=result.customer.payment_methods[0].token)
    d.session.add(subscription)
    user.profile.plan = 'pro'
    d.session.commit()

    # Now that we have enough info to start the subscription, activate it.
    return _activate_subscription(subscription, user, role_slug)


def _activate_subscription(subscription, user, role_slug):
    plan_info = plan.get(role_slug, subscription.plan_type)

    plan_id = ''
    if subscription.plan_length == 'annual':
        plan_id = plan_info['annual_plan_id']
    else:
        plan_id = plan_info['monthly_plan_id']

    if not plan_id:
        raise UserWarning("Invalid plan")

    result = braintree.Subscription.create({
        'payment_method_token': subscription.payment_method_token,
        'plan_id': plan_id})

    print result

    if not result.is_success:
        return result

    subscription.status = 'active'
    subscription.next_payment_due = result.subscription.next_billing_date
    subscription.braintree_subscription_id = result.subscription.id
    user.profile.plan = subscription.plan_type
    d.session.commit()
    emails.subscription_invoice.delay(subscription.id)
    return result


def deactivate_subscription(user):
    subscription = _subscription_object(user)
    if subscription:
        result = braintree.Subscription.cancel(subscription.braintree_subscription_id)
        user.profile.plan = 'intro'
        subscription.status = 'ended'
        d.session.commit()
        return result


def get_subscription(user):
    subscription = _subscription_object(user)
    if subscription:
        return braintree.Subscription.find(subscription.braintree_subscription_id)
    return None


def _subscription_object(user):
    return (db.UserSubscription.query
            .filter_by(user_id=user.id)
            .filter_by(active=True)
            .filter_by(status='active')
            .order_by('-id')
            .first())


def subscription_due(subscription_id):
    subscription = (db.UserSubscription.query
                    .filter_by(active=True)
                    .filter_by(braintree_subscription_id=subscription_id)
                    .first())

    if not subscription:
        sentry.captureMessage("Subscription not found: " + str(subscription_id))
        return

    if subscription.status == 'active':
        subscription.status = 'overdue'
        subscription.user.profile.plan = 'intro'
        d.session.commit()


def recurring_subscription(webhook_notification):
    subscription = (db.UserSubscription.query
                    .filter_by(active=True)
                    .filter_by(braintree_subscription_id=webhook_notification.subscription.id)
                    .first())
    subscription.next_payment_due = webhook_notification.subscription.billing_period_end_date
    d.session.commit()


def pro_plan(user):
    if not user.profile.role.name == 'Athlete':
        subscription = _subscription_object(user)
        if subscription:
            if subscription.plan_type == 'pro':
                return True
            else:
                return False
        else:
            return False
    else:
        return True
