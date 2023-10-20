# class StateCityTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.state = State.objects.create(name="Test state")
#         self.city = City.objects.create(name="Test city", state=self.state)

#     def test_state_city_list_api(self):
#         response = self.client.get(STATE_CITY_LIST_URL)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         expected_data = StateCityListSerilizer([self.state], many=True).data
#         self.assertEqual(response.data, expected_data)


# class AddressViewsTests(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             username="testuser", email="test@gmail.com", password="testpass"
#         )
#         self.client = APIClient()
#         tokens = generate_jwt_token(self.user)
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

#         self.address = Address.objects.create(
#             user=self.user,
#             state="Test State",
#             city="Test City",
#             phone="09012342134",
#             postal_code="1847382365",
#             street_address="Test street address",
#             house_number="434",
#         )
#         self.ADDRESS_RUD_URL = reverse(
#             "accounts:address-detail", args=[self.address.pk]
#         )

#     def test_list_user_address_api(self):
#         response = self.client.get(ADDRESS_LIST_CREATE_URL)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         expected_data = AddressSerializer([self.address], many=True).data
#         self.assertEqual(response.data, expected_data)

#     def test_address_create_api(self):
#         payload = {
#             "user": self.user,
#             "state": "Test State",
#             "city": "Test City",
#             "phone": "09012452123",
#             "postal_code": "1847382365",
#             "street_address": "Test street address",
#             "house_number": "434",
#         }
#         response = self.client.post(ADDRESS_LIST_CREATE_URL, payload)

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Address.objects.count(), 2)
#         self.assertTrue(Address.objects.filter(phone="09012452123").exists())

#     def test_address_retrieve_api(self):
#         response = self.client.get(self.ADDRESS_RUD_URL)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         expected_data = AddressSerializer(self.address).data
#         self.assertEqual(response.data, expected_data)

#     def test_address_update_api(self):
#         payload = {"state": "updated state", "city": "updated city"}
#         response = self.client.patch(self.ADDRESS_RUD_URL, payload)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         address = Address.objects.get(pk=self.address.pk)
#         self.assertEqual(address.state, "updated state")
#         self.assertEqual(address.city, "updated city")

#     def test_address_delete_api(self):
#         response = self.client.delete(self.ADDRESS_RUD_URL)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Address.objects.filter(pk=self.address.pk).exists())