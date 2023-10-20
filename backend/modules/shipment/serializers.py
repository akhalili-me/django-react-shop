from rest_framework import serializers
from .models import State,Address


class StateCityListSerilizer(serializers.ModelSerializer):
    cities = serializers.StringRelatedField(many=True)

    class Meta:
        model = State
        fields = ["name", "cities"]

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "state",
            "city",
            "phone",
            "postal_code",
            "street_address",
            "house_number",
        ]