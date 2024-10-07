from django.db import models
from django.conf import settings  # This is to reference the CustomUser model


class SubscriptionPlan(models.Model):
    PLAN_TYPES = [
        ("free", "Free"),
        ("premium", "Premium"),
        ("golden", "Golden"),
    ]
    type = models.CharField(max_length=10, choices=PLAN_TYPES)
    duration = models.IntegerField()  # Duration in months
    price = models.DecimalField(
        max_digits=6, decimal_places=2
    )  # You can adjust price format if needed

    def __str__(self):
        return f"{self.type} - {self.duration} months"


# Payment Model
class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("successful", "Successful"),
        ("failed", "Failed"),
    ]
    subscriptionplan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.DO_NOTHING
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    payment_status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS_CHOICES, default="pending"
    )
    payment_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.get_payment_status_display()}"


# Refund Model
class Refund(models.Model):
    REFUND_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("successful", "Successful"),
        ("failed", "Failed"),
    ]

    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE
    )  # Link to the Payment model
    refund_id = models.CharField(
        max_length=255, null=True, blank=True
    )  # Zibal refund ID
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount refunded
    refund_status = models.CharField(
        max_length=10, choices=REFUND_STATUS_CHOICES, default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Refund {self.refund_id} - {self.get_refund_status_display()}"


# Subscription Payment Model
class SubscriptionPayment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subs_payment"
    )  # Link to the CustomUser model
    subscription_plan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.CASCADE
    )  # Link to SubscriptionPlan model in user app
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE
    )  # Link to the Payment model
    start_date = models.DateField()  # Subscription start date
    end_date = models.DateField()  # Subscription end date
    is_active = models.BooleanField(
        default=True
    )  # Check if subscription is still active

    def __str__(self):
        return f"Subscription for {self.user.username} - Plan {self.subscription_plan.type}"
