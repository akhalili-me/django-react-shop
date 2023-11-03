from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import UserAddress, State, City
from django.db import IntegrityError

from modules.utility.factories import UserFactory


class AddressTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.address = UserAddress.objects.create(
            user=self.user,
            state="Test State",
            city="Test City",
            phone="09012342134",
            postal_code="1847382365",
            street_address="Test street address",
            house_number="434",
        )

    def test_address_creation(self):
        self.assertEqual(UserAddress.objects.count(), 1)
        self.assertEqual(self.address.user, self.user)
        self.assertEqual(self.address.state, "Test State")
        self.assertEqual(self.address.city, "Test City")
        self.assertEqual(self.address.phone, "09012342134")
        self.assertEqual(self.address.postal_code, "1847382365")
        self.assertEqual(self.address.street_address, "Test street address")
        self.assertEqual(self.address.house_number, "434")

    def test_phone_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            UserAddress.objects.create(
                user=self.user,
                state="Test State",
                city="Test City",
                phone="09012342134",
                postal_code="1847382365",
                street_address="Test street address",
                house_number="434",
            )

    def test_address_update(self):
        self.address.state = "updated state"
        self.address.street_address = "updated street address"
        self.address.save()

        updated_address = UserAddress.objects.get(pk=self.address.pk)

        self.assertEqual(updated_address.state, "updated state")
        self.assertEqual(updated_address.street_address, "updated street address")

    def test_address_delete(self):
        self.address.delete()
        self.assertFalse(UserAddress.objects.filter(pk=self.address.pk).exists())


class StateTestCase(TestCase):
    def setUp(self):
        self.state = State.objects.create(name="Test state")

    def test_state_creation(self):
        self.assertEqual(State.objects.count(), 1)
        self.assertEqual(self.state.name, "Test state")

    def test_state_update(self):
        self.state.name = "updated name"
        self.state.save()

        updated_state = State.objects.get(pk=self.state.pk)

        self.assertEqual(updated_state.name, "updated name")

    def test_state_delete(self):
        self.state.delete()
        self.assertFalse(State.objects.filter(pk=self.state.pk).exists())


class CityTestCase(TestCase):
    def setUp(self):
        self.state = State.objects.create(name="Test state")
        self.city = City.objects.create(name="Test city", state=self.state)

    def test_city_creation(self):
        self.assertEqual(City.objects.count(), 1)
        self.assertEqual(self.city.state, self.state)
        self.assertEqual(self.city.name, "Test city")

    def test_city_update(self):
        self.city.name = "updated name"
        self.city.save()

        updated_city = City.objects.get(pk=self.city.pk)

        self.assertEqual(updated_city.name, "updated name")

    def test_city_delete(self):
        self.city.delete()
        self.assertFalse(City.objects.filter(pk=self.city.pk).exists())
