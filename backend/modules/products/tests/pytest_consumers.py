from channels.testing import WebsocketCommunicator
from ..consumers import ProductConsumer
import pytest
from channels.layers import get_channel_layer

@pytest.mark.asyncio
async def test_product_consumer():
    communicator = WebsocketCommunicator(ProductConsumer.as_asgi(), "/ws/product_update")
    connected, _ = await communicator.connect()
    assert connected

    await communicator.send_json_to({
        "type": "price_update", 
        "message": {"product_id":1, "new_price": 178}
    })
    response = await communicator.receive_json_from()
    print(response)
    assert response["type"] == "price_update"
    assert response["message"]["product_id"] == 1
    assert response["message"]["new_price"] == 178
    await communicator.disconnect()
