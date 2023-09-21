from channels.generic.websocket import AsyncJsonWebsocketConsumer

class ProductConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("product_updates", self.channel_name)
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("product_updates", self.channel_name)
    
    async def receive_json(self, content):
        type = content["type"]
        await self.channel_layer.group_send("product_updates",{"type": type,"content": content})
 
    async def price_update(self, event):
        await self.send_json(content=event["content"])
  