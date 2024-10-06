from dj_rest_auth.registration.views import RegisterView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomRegisterSerializer, SubscriptionPlanSerializer
from .models import SubscriptionPlan
from rest_framework import viewsets, status



class CustomRegisterViewSet(viewsets.ViewSet):
    """
    A viewset for registering a new user with an additional phone number field.
    """

    serializer_class = CustomRegisterSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save(request)
            return Response(
                {
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "phone_number": user.phone_number,
                    }
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubscriptionPlanViewSet(viewsets.ViewSet):
    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.objects.all()