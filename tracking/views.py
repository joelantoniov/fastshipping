from rest_framework import generics
from .models import PackageStatus
from .serializers import PackageStatusSerializer

class PackageStatusListCreateView(generics.ListCreateAPIView):
    queryset = PackageStatus.objects.all()
    serializer_class = PackageStatusSerializer

class PackageStatusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PackageStatus.objects.all()
    serializer_class = PackageStatusSerializer
