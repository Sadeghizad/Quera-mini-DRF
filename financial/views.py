from .models import Payment, SubscriptionPlan
from .utils import subscriptions
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView
from .serializers import InitiatePaymentSerializer
from django.shortcuts import get_object_or_404


class InitiatePaymentView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = InitiatePaymentSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        user = request.user
        subscriptionplan_id = request.data.get("subscriptionplan")

        # Get the subscription plan instance
        subscriptionplan = get_object_or_404(SubscriptionPlan, id=subscriptionplan_id)

        # Create payment object with the amount from subscription plan
        payment = Payment.objects.create(
            user=user,
            subscriptionplan=subscriptionplan,
            amount=subscriptionplan.price,  # Set amount from the subscription plan's price
        )

        # Mocked IPG URL (replace with actual IPG URL if needed)
        ipg_url = "https://mocki.io/v1/ddb70dbe-6f3c-4499-8737-6bbe1dd390fa"
        data = {
            "LoginAccount": "login_account",
            "Amount": payment.amount,
            "CallBackUrl": "https://domain.com/payment/callback/",
        }

        # Mock response from the IPG (change to `requests.post` for actual IPG)
        # ipg_url = "https://pec.shaparak.ir/NewIPGServices/Sale/SaleService.asmx"
        response = requests.get(ipg_url)
        token = response.json().get("Token")
        if token:
            payment.payment_url = f"https://pec.shaparak.ir/NewIPG/?token={token}"
            payment.save()
            return Response({"redirect_url": payment.payment_url})
        else:
            return Response({"error": "Payment initiation failed"}, status=400)


class PaymentCallbackView(APIView):
    def post(self, request):
        payment_id = request.data.get("PaymentId")
        status = request.data.get("status")
        rrn = request.data.get("RRN")

        # if request.host == 'https:\\folan.ir':
        #     return Response({"error":"your not from the bank mr\mrs chucky"})

        if not payment_id or not status or not rrn:
            return Response({"error": "Missing required fields"}, status=400)

        try:
            payment = Payment.objects.get(id=payment_id)
            if status == "0" and int(rrn) > 0:
                payment.payment_status = "successful"
                subscriptions(payment, payment.user, payment.subscriptionplan)
            else:
                payment.payment_status = "failed"
            payment.save()
            return Response({"message": "Payment status updated successfully"})
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)
