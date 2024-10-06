from rest_framework.routers import DefaultRouter
from .views import initiate_payment, payment_callback
from django.urls import path, include
router = DefaultRouter()
urlpatterns = [
    path('payment/initiate/', initiate_payment, name='initiate_payment'),
    path('payment/callback/', payment_callback, name='payment_callback'),
    path('', include(router.urls)),
]