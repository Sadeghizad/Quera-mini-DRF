from rest_framework.routers import DefaultRouter
from .views import InitiatePaymentView, PaymentCallbackView
from .viewsets import SubscriptionPlanViewSet
from django.urls import path, include
router = DefaultRouter()
router.register(r'subscriptionplans', SubscriptionPlanViewSet, basename='subscriptionplan')
urlpatterns = [
    path('payment/initiate/', InitiatePaymentView.as_view(), name='initiate_payment'),
    path('payment/callback/', PaymentCallbackView.as_view(), name='payment_callback'),
    path('', include(router.urls)),
]