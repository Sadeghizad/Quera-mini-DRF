from .models import Payment, SubscriptionPlan, Refund
from .utils import subscriptions
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView
from .serializers import InitiatePaymentSerializer, RefundSerializer
from django.shortcuts import get_object_or_404
from datetime import timedelta
from django.utils import timezone
from decimal import Decimal
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


class InitiateRefundView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RefundSerializer
    def get(self, request, *args, **kwargs):
        user=request.user
        refunds = Refund.objects.filter(payment__user=user)
        serializer = self.serializer_class(refunds, many=True)  # Serialize the refunds
        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        payment_id = request.data.get('payment_id')

        # Ensure the payment exists and belongs to the user
        payment = get_object_or_404(Payment, id=payment_id, user=request.user)

        # Check if a refund is already in process or completed
        if Refund.objects.filter(payment=payment).exists():
            return Response({"error": "Refund already processed or in process"}, status=400)

        # Check if the refund amount is valid
        time_difference = timezone.now() - payment.created_at
        if time_difference <= timedelta(days=1):
            refund_amount = payment.amount
        elif time_difference <= timedelta(days=3):
            refund_amount = payment.amount * Decimal(0.8)
        elif time_difference <= timedelta(days=7):
            refund_amount = payment.amount * Decimal(0.5)
        elif time_difference <= timedelta(days=10):
            refund_amount = payment.amount * Decimal(0.2)
        elif time_difference <= timedelta(days=14):
            refund_amount = 0
        else:
            return Response({"error": "Refund period expired"}, status=400)

        # Create the refund object
        refund = Refund.objects.create(
            payment=payment,
            amount=refund_amount,
            refund_status="pending"  # Set status as pending initially
        )

        # a function to add amount to wallet or call bank api to send money
        def cash_handle_some_how():
            pass
        #mock the refund as successful
        refund.refund_status = "successful"
        # refund.refund_status = "failed"
        refund.save()
        subscription = payment.subscription.get()
        if subscription:
            subscription.is_active = False
            subscription.save()
        return Response({"message": "Refund initiated successfully", "refund_id": refund.id})
