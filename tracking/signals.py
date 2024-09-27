from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import PackageStatus
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=PackageStatus)
def broadcast_status_update(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    group_name = f'shipment_{instance.shipment.id}'
    
    try:
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'chat_message',
                'message': instance.status,
            }
        )
        logger.info(f"Message sent to {group_name}: {instance.status}")
    except Exception as e:
        logger.error(f"Failed to broadcast status update: {e}")

