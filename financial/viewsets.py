from .models import SubscriptionPlan, Payment
from .serializers import SubscriptionPlanSerializer, PaymentHistorySerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.objects.all()

class PaymentHistory(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentHistorySerializer

    def get_queryset(self):
        # Filter payments by the authenticated user
        return Payment.objects.filter(user=self.request.user)