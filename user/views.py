from django.shortcuts import render
from .serializers import CustomLoginSerializer
from dj_rest_auth.views import LoginView

class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer
