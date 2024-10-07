from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Custom User Model
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15)
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

