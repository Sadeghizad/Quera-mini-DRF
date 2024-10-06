from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Subscription Plan Model
class SubscriptionPlan(models.Model):
    PLAN_TYPES = [
        ('free', 'Free'),
        ('premium', 'Premium'),
        ('golden', 'Golden'),
    ]
    type = models.CharField(max_length=10, choices=PLAN_TYPES)
    duration = models.IntegerField()  # Duration in months
    price = models.DecimalField(max_digits=6, decimal_places=2)  # You can adjust price format if needed

    def __str__(self):
        return f"{self.type} - {self.duration} months"

# Custom User Model
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
    # Add related_name arguments for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Avoid conflicts
        blank=True,
        help_text='The groups this user belongs to.'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Avoid conflicts
        blank=True,
        help_text='Specific permissions for this user.'
    )

