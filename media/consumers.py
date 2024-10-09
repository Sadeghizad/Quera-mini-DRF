import json
from channels.generic.websocket import AsyncWebsocketConsumer


class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.video_id = self.scope["url_route"]["kwargs"]["video_id"]
        self.room_group_name = f"video_{self.video_id}"

        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    
    async def video_update(self, event):
        action = event["action"]
        data = event["data"]

        
        await self.send(text_data=json.dumps({"action": action, "data": data}))

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the comment group
        self.room_group_name = 'comments'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the comment group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        comment = text_data_json['comment']

        # Broadcast the comment to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'comment_message',
                'comment': comment
            }
        )

    # Receive message from group
    async def comment_message(self, event):
        comment = event['comment']

        # Send the comment to WebSocket
        await self.send(text_data=json.dumps({
            'comment': comment
        }))