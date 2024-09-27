from rest_framework import generics, status
from rest_framework.response import Response
from .models import PackageStatus
from shipping_management.models import Shipment
from .serializers import PackageStatusSerializer

class PackageStatusListCreateView(generics.ListCreateAPIView):
    queryset = PackageStatus.objects.all()
    serializer_class = PackageStatusSerializer

class PackageStatusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PackageStatus.objects.all()
    serializer_class = PackageStatusSerializer

class PackageStatusByTrackingNumberView(generics.GenericAPIView):

    serializer_class = PackageStatusSerializer

    def get(self, request, tracking_number, *args, **kwargs):
        try:
            shipment = Shipment.objects.get(tracking_number=tracking_number)
            statuses = PackageStatus.object.filter(shipment=shipment)
            serializer = self.get_serializer(statuses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Shipment.DoesNotExist:
            return Response({"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)
