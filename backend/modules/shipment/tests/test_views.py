from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from ..serializers import StateCityListSerilizer, AddressSerializer
from ..models import State, UserAddress, City
from modules.utility.factories import UserFactory, UserAddressFactory
from modules.utility.tokens import apply_jwt_token_credentials_to_client

STATE_CITY_LIST_URL = reverse("shipment:locations-list")
ADDRESS_LIST_CREATE_URL = reverse("shipment:user-address-create-list")


class StateCityTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.state = State.objects.create(name="Test state")
        self.city = City.objects.create(name="Test city", state=self.state)

    def test_state_city_list_api(self):
        response = self.client.get(STATE_CITY_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = StateCityListSerilizer([self.state], many=True).data
        self.assertEqual(response.data, expected_data)


class AddressViewsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        apply_jwt_token_credentials_to_client(self.client, self.user)
        self.address = UserAddressFactory(user=self.user)

    def test_list_user_address_api(self):
        response = self.client.get(ADDRESS_LIST_CREATE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = AddressSerializer([self.address], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_address_create_api(self):
        payload = {
            "user": self.user,
            "state": "Test State",
            "city": "Test City",
            "phone": "09012452123",
            "postal_code": "1847382365",
            "street_address": "Test street address",
            "house_number": "434",
        }
        response = self.client.post(ADDRESS_LIST_CREATE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserAddress.objects.count(), 2)
        self.assertTrue(UserAddress.objects.filter(phone="09012452123").exists())

    def test_address_retrieve_api(self):
        response = self.client.get(self.address.get_absolute_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = AddressSerializer(self.address).data
        self.assertEqual(response.data, expected_data)

    def test_address_update_api(self):
        payload = {"state": "updated state", "city": "updated city"}
        response = self.client.patch(self.address.get_absolute_url(), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        address = UserAddress.objects.get(pk=self.address.pk)
        self.assertEqual(address.state, "updated state")
        self.assertEqual(address.city, "updated city")

    def test_address_delete_api(self):
        response = self.client.delete(self.address.get_absolute_url())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserAddress.objects.filter(pk=self.address.pk).exists())
