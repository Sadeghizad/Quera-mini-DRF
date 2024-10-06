def is_subscription_active(user):
    current_date = timezone.now().date()
    active_subscription = Subscription.objects.filter(user=user, is_active=True, end_date__gte=current_date).exists()
    return active_subscription

from datetime import timedelta
from django.utils import timezone
from .models import Subscription, Payment

def renew_subscriptions():
    current_date = timezone.now().date()
    expiring_soon = Subscription.objects.filter(is_active=True, end_date__lt=current_date + timedelta(days=3))
    
    for subscription in expiring_soon:
        # Charge the user again using your payment gateway
        payment_success = process_payment(subscription.user, subscription.subscription_plan)
        
        if payment_success:
            # Update the subscription end date
            subscription.end_date += timedelta(days=subscription.subscription_plan.duration)  # assuming duration is in days
            subscription.save()
        else:
            subscription.is_active = False
            subscription.save()
