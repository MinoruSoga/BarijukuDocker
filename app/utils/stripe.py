import stripe
from django.conf import settings
import logging

logger = logging.getLogger()


class Stripe():
    def __init__(self):
        stripe.api_key = settings.STRIPE_CLIENT_SECRET
        
    def modify_cancel_subscription(self, subscription_id):
        subscription = stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=True
        )
        return subscription
    def modify_not_cancel_subscription(self, subscription_id):
        subscription = stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=False
        )
        return subscription
