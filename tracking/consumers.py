from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging

logger = logging.getLogger(__name__)

class TrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.shipment_id = self.scope['url_route']['kwargs']['shipment_id']
        self.room_group_name = f'shipment_{self.shipment_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        logger.info(f"WebSocket connected: {self.channel_name} to {self.room_group_name}")
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        logger.info(f"WebSocket disconnected: {self.channel_name} from {self.room_group_name}")

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            # Validate message format
            if not isinstance(message, str):
                raise ValueError("Message must be a string.")

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        except ValueError as e:
            logger.error(f"Invalid message format: {e}")
            await self.send(text_data=json.dumps({
                'error': f"Invalid message format: {e}"
            }))
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON message.")
            await self.send(text_data=json.dumps({
                'error': "Invalid JSON format."
            }))
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            await self.send(text_data=json.dumps({
                'error': "An unexpected error occurred."
            }))

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

