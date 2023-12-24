import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DeviceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope['url_route'])
        self.room_name = self.scope['url_route']['kwargs']['uuid']
        
        print(self.room_name)
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data['type']

        if message_type == 'device.message':
            await self.send_to_group_device(data['message'],message_type)
        elif message_type == 'pin.message':
            await self.send_to_group_pin(data['message'],message_type,data['pin'],data['state'])

    async def send_to_group_device(self, message,msg_type):
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': msg_type,
                'message': message
            }
        )


    async def send_to_group_pin(self, message,msg_type,pin,state):
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': msg_type,
                'message': message,
                'pin':pin,
                'state':state
            }
        )
    
    async def device_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'device.message',
            'message': event['message']
        }))
    async def pin_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'pin.message',
            'message': event['message'],
            'pin': event['pin'],
            'state': event['state'],
        }))
