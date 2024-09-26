from django.db import models
from shipping_management.models import Shipment

class PackageStatus(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='statuses')
    status = models.CharField(max_length=100)
    location = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.shipment.tracking_number} - {self.status}'
