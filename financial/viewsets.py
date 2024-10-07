from .models import SubscriptionPlan
from .serializers import SubscriptionPlanSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.objects.all()