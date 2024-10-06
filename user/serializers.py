from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import CustomUser  # Make sure to use your custom user model
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from .models import *
from media.models import Video

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number', 'subscription_plan']

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'type', 'duration', 'price']



class CustomRegisterSerializer(RegisterSerializer):
    phone_number = serializers.CharField(required=True)
    def validate_phone_number(self, value):
        if CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("A user with this phone number already exists.")
        return value
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    def get_cleaned_data(self):
        data = super().get_cleaned_data()  # Reuse parent class method to get the default cleaned data
        data['phone_number'] = self.validated_data.get('phone_number', '')
        return data

    def save(self, request):
        user = super().save(request)  # Call the parent class save method
        self.cleaned_data = self.get_cleaned_data()

        # Assign the additional phone_number field to the user object
        user.phone_number = self.cleaned_data.get('phone_number')
        user.save()  # Save the user object after assigning the phone number

        return user



class CustomLoginSerializer(LoginSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})

    def validate(self, data):
        # Check if one of username, email, or phone number is provided
        username = data.get('username')
        email = data.get('email')
        phone_number = data.get('phone_number')
        password = data.get('password')

        if not username and not email and not phone_number:
            raise serializers.ValidationError(_("One of username, email, or phone number must be provided."))

        user = None
        if username:
            user = authenticate(username=username, password=password)
        elif email:
            user = authenticate(email=email, password=password)
        elif phone_number:
            try:
                user_obj = CustomUser.objects.get(phone_number=phone_number)
                user = authenticate(username=user_obj.username, password=password)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError(_("Invalid phone number."))

        if not user:
            raise serializers.ValidationError(_("Invalid credentials or account is not active."))

        # Email verification check
        # if email and not user.emailaddress_set.filter(verified=True).exists():
        #     raise serializers.ValidationError(_("E-mail is not verified."))

        if user and not user.is_active:
            raise serializers.ValidationError(_("This account is inactive."))

        return {'user': user}

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = "__all__"