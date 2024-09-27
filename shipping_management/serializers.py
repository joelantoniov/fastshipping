#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from .models import Shipment
from rest_framework import serializers

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'

    def validate(self, data):
        # Validate origin address
        response_origin = requests.post(
            "http://127.0.0.1:8000/api/addresses/validate-address/",
            json={"address": data['origin_address']}
        )

        # Check if the response is not empty and valid JSON
        try:
            response_origin_json = response_origin.json()
        except ValueError:
            raise serializers.ValidationError("Failed to validate origin address. Invalid response from the address validation service.")

        if not response_origin_json.get('valid'):
            raise serializers.ValidationError("Invalid origin address.")

        # Validate destination address
        response_destination = requests.post(
            "http://127.0.0.1:8000/api/addresses/validate-address/",
            json={"address": data['destination_address']}
        )

        try:
            response_destination_json = response_destination.json()
        except ValueError:
            raise serializers.ValidationError("Failed to validate destination address. Invalid response from the address validation service.")

        if not response_destination_json.get('valid'):
            raise serializers.ValidationError("Invalid destination address.")

        return data

