from rest_framework.routers import DefaultRouter
from .views import InitiatePaymentView, PaymentCallbackView, InitiateRefundView
from .viewsets import SubscriptionPlanViewSet,PaymentHistory
from django.urls import path, include
router = DefaultRouter()
router.register(r'subscriptionplans', SubscriptionPlanViewSet, basename='subscriptionplan')
router.register(r'payment/history', PaymentHistory, basename='payment-history')
urlpatterns = [
    path('payment/initiate/', InitiatePaymentView.as_view(), name='initiate_payment'),
    path('payment/callback/', PaymentCallbackView.as_view(), name='payment_callback'),
    path('', include(router.urls)),
    path('payment/refund/', InitiateRefundView.as_view(), name='initiate_refund'),
]

