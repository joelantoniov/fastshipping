from rest_framework import generics
from .models import Shipment
from .serializers import ShipmentSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class ShipmentListCreateView(generics.ListCreateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

def update_tracking_status(shipment_id, status, location):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
            f"shipment_{shipment_id}",
            {
                "type": "shipment.update",
                "status": status,
                "location": location,
            }
    )

class ShipmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        update_tracking_status(
                instance.id,
                instance.status,
                instance.location
                #instance.origin_address
        )
