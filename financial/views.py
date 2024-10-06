from django.shortcuts import redirect
from django.http import JsonResponse
from .models import Payment
import requests


# Function to initiate payment
def initiate_payment(request):
    user = request.user  # Get the authenticated user
    amount = request.POST.get("amount")  # Get payment amount from request

    # Prepare data to send to payment gateway (e.g., Parsian IPG)
    order_id = "unique_order_id"
    payment = Payment.objects.create(user=user, amount=amount, order_id=order_id)

    # Send request to IPG (Parsian IPG example)
    ipg_url = "https://pec.shaparak.ir/NewIPGServices/Sale/SaleService.asmx"
    data = {
        "LoginAccount": "login_account",
        "Amount": payment.amount,
        "OrderId": payment.order_id,
        "CallBackUrl": "https://domain.com/payment/callback/",
    }

    # Make request to IPG
    response = requests.post(ipg_url, data=data)
    token = response.json().get("Token")

    if token:
        payment.payment_url = f"https://pec.shaparak.ir/NewIPG/?token={token}"
        payment.save()
        return redirect(payment.payment_url)  # Redirect user to payment gateway
    else:
        return JsonResponse({"error": "Payment initiation failed"}, status=400)


# Function to handle payment callback
def payment_callback(request):
    order_id = request.POST.get("OrderId")
    status = request.POST.get("status")
    rrn = request.POST.get("RRN")

    try:
        payment = Payment.objects.get(order_id=order_id)
        if status == "0" and int(rrn) > 0:
            payment.payment_status = "successful"
        else:
            payment.payment_status = "failed"
        payment.save()
        return JsonResponse({"message": "Payment updated successfully"})
    except Payment.DoesNotExist:
        return JsonResponse({"error": "Payment not found"}, status=404)
