from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Address
from .serializers import AddressSerializer
from django.core.cache import cache

class AddressListCreateView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class ValidateAddressView(APIView):
    def post(self, request, *args, **kwargs):
        address = request.data.get('address')

        # check cache first
        cached_result = cache.get(address)
        if cached_result:
            return Response(cached_result, status=status.HTTP_200_OK)

        if "Street" in address:
            result = {"valid": True, "message": "Address is valid."}
        else:
            result = {"valid": False, "message": "Invalid address."}

        cache.set(address, result, timeout=60*60) # Cache for 1 hour
        return Response(result, status=status.HTTP_200_OK if result["valid"] else status.HTTP_400_BAD_REQUEST)
