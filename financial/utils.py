from datetime import timedelta
from django.utils import timezone
from .models import  Payment,SubscriptionPayment
def is_subscription_active(user):
    current_date = timezone.now().date()
    active_subscription = SubscriptionPayment.objects.filter(user=user, is_active=True, end_date__gte=current_date).exists()
    return active_subscription


def subscriptions(payment,user, subscription_plan):
    current_date = timezone.now().date()
    
    
    last_sub = user.subs_payment.all().order_by('-id').first()

    if last_sub and last_sub.is_active:  
        SubscriptionPayment.objects.create(
            user=user,
            payment=payment,
            subscription_plan=subscription_plan,
            start_date=last_sub.end_date,
            end_date=last_sub.end_date + timedelta(days=subscription_plan.duration)
        )
    else:
        SubscriptionPayment.objects.create(
            user=user,
            payment=payment,
            subscription_plan=subscription_plan,
            start_date=current_date,
            end_date=current_date + timedelta(days=subscription_plan.duration)
        )
