from rest_framework import serializers
from .models import Discount


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = [
            "id",
            "name",
            "user",
            "type",
            "code",
            "usage_limit",
            "value",
            "min_purchase_amount",
            "expire_at",
        ]

    def validate(self, attrs):
        super().validate(attrs)
        type = attrs.get("type")
        value = attrs.get("value")

        if type == "percentage" and value > 100:
            raise serializers.ValidationError(
                "Percentage discount cannot be greater than 100%."
            )

        return attrs
