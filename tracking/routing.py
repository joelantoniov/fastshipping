#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
        re_path(r'ws/tracking/(?P<shipment_id>\d+)/$', consumers.TrackingConsumer.as_asgi()),  # Corrected pattern and method
]
