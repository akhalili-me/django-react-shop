from channels.testing import WebsocketCommunicator
from ..consumers import ProductConsumer
from django.test import TestCase

class ProductConsumerTests(TestCase):

    async def test_price_update_event(self):
        communicator = WebsocketCommunicator(ProductConsumer.as_asgi(), "/ws/product_update")
        connected, _ = await communicator.connect()
        self.assertTrue(connected) 

        await communicator.send_json_to({
            "type": "price_update", 
            "content": {"product_id":1, "new_price": 178}
        })
        response = await communicator.receive_json_from()
        self.assertEqual(response["type"],"price_update")
        self.assertEqual(response["content"]["product_id"],1)
        self.assertEqual(response["content"]["new_price"],178)
        await communicator.disconnect()