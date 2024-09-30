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
            # Parse JSON message
            text_data_json = json.loads(text_data)

            # Check message type and handle accordingly
            message_type = text_data_json.get('type')
            
            if message_type == "tracking_update":
                status = text_data_json.get('status')
                location = text_data_json.get('location')
                if not status or not location:
                    raise ValueError("Both 'status' and 'location' must be provided for tracking updates.")

                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'tracking_update',
                        'status': status,
                        'location': location
                    }
                )
            else:
                raise ValueError(f"Unsupported message type: {message_type}")
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

    async def tracking_update(self, event):
        status = event['status']
        location = event['location']

        # Send the tracking update to WebSocket
        await self.send(text_data=json.dumps({
            'status': status,
            'location': location
        }))
