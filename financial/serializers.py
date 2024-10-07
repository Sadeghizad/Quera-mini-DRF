from rest_framework import serializers
from .models import *

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'amount', 'transaction_id', 'payment_status', 'order_id', 'created_at']
class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = ['id', 'payment', 'refund_id', 'amount', 'refund_status', 'created_at']

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = "__all__"
class InitiatePaymentSerializer(serializers.ModelSerializer):
    subscriptionplan = serializers.PrimaryKeyRelatedField(queryset=SubscriptionPlan.objects.all())
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Payment
        fields = ['subscriptionplan', 'amount']

    def create(self, validated_data):
        user = self.context['request'].user
        payment = Payment.objects.create(
            user=user,
            subscriptionplan=validated_data['subscriptionplan'],
            amount=validated_data['amount'],
        )
        return payment