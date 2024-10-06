from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'amount', 'transaction_id', 'payment_status', 'order_id', 'created_at']  # Expose relevant payment details
class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = ['id', 'payment', 'refund_id', 'amount', 'refund_status', 'created_at']