from rest_framework import serializers
from .models import *


class InitiatePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "subscriptionplan", "transaction_id", "created_at"]
        read_only_fields = ["id", "transaction_id", "created_at"]


class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = ["id", "payment", "refund_id", "amount", "refund_status", "created_at"]


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = "__all__"


class InitiatePaymentSerializer(serializers.ModelSerializer):
    subscriptionplan = serializers.PrimaryKeyRelatedField(
        queryset=SubscriptionPlan.objects.all()
    )
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Payment
        fields = ["subscriptionplan", "amount"]

    def create(self, validated_data):
        user = self.context["request"].user
        payment = Payment.objects.create(
            user=user,
            subscriptionplan=validated_data["subscriptionplan"],
            amount=validated_data["amount"],
        )
        return payment


class PaymentHistorySerializer(serializers.ModelSerializer):
    subscriptionplan_type = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            "subscriptionplan_type",  # Show the type instead of the whole subscriptionplan object
            "transaction_id",
            "updated_at",
            "amount",
            "payment_status",
        ]
        read_only_fields = fields

    def get_subscriptionplan_type(self, obj):
        return obj.subscriptionplan.type