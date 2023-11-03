from django.test import TestCase
from modules.utility.factories import CommentFactory, ProductFactory


class CommentSignalTests(TestCase):
    def setUp(self):
        self.product = ProductFactory()
        for i in range(2):
            CommentFactory(product=self.product, rate=i + 1)

    def test_product_update_rate(self):
        self.assertEqual(self.product.rate, 1.5)
