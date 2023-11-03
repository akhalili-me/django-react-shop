from django.test import TestCase
from django.core.cache import cache
from channels.testing import WebsocketCommunicator
from ..consumers import ProductConsumer
from asgiref.sync import sync_to_async
from modules.utility.factories import CommentFactory, ProductFactory


class ProductSignalTests(TestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.comment1 = CommentFactory(product=self.product)
        self.comment2 = CommentFactory(product=self.product)
        self.SORT_CHOICES = ("newest", "bestselling", "most_viewed")
        for sort in self.SORT_CHOICES:
            cache.set(f"product_list_{sort}", "sample data")

    def test_product_update_rate_after_comment_creation(self):
        excepted_rate = (self.comment1.rate + self.comment2.rate) / 2
        self.assertEqual(self.product.rate, excepted_rate)

    def test_cache_delete_after_comment_creation(self):
        CommentFactory()
        for sort in self.SORT_CHOICES:
            self.assertIsNone(cache.get(f"product_list_{sort}"))

    def test_product_update_rate_after_comment_delete(self):
        self.comment1.delete()
        self.assertEqual(self.product.rate, self.comment2.rate)

    def test_cache_delete_after_comment_delete(self):
        self.comment1.delete()
        for sort in self.SORT_CHOICES:
            self.assertIsNone(cache.get(f"product_list_{sort}"))

    async def test_price_update_singal_channel_layers_message(self):
        communicator = WebsocketCommunicator(
            ProductConsumer.as_asgi(), "/ws/product_update"
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        self.product.price = 50
        await sync_to_async(self.product.save)()
        response = await communicator.receive_json_from()
        self.assertEqual(response["product_id"], self.product.pk)
        self.assertEqual(response["new_price"], float(50))
