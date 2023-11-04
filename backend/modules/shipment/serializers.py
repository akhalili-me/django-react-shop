from rest_framework import serializers
from .models import State, UserAddress


class StateCityListSerilizer(serializers.ModelSerializer):
    cities = serializers.StringRelatedField(many=True)

    class Meta:
        model = State
        fields = ["name", "cities"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = [
            "uuid",
            "state",
            "city",
            "phone",
            "postal_code",
            "street_address",
            "house_number",
        ]
