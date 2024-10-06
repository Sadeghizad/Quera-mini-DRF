from django.urls import path, include
from django.contrib.auth import views
from rest_framework.routers import DefaultRouter
from .viewsets import CustomRegisterViewSet
from .views import CustomLoginView

router = DefaultRouter()
router.register(r'registration', CustomRegisterViewSet, basename='registration')


urlpatterns = [
    path('auth/login/', CustomLoginView.as_view(), name='custom_login'),
    path('auth/', include(router.urls)),
    path('auth/', include('dj_rest_auth.urls')),
    path(
        'auth/password/reset/confirm/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
]