#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
        path('shipments/', views.ShipmentListCreateView.as_view(), name='shipment-list-create'),
        path('shipments/<int:pk>/', views.ShipmentDetailView.as_view(), name='shipment-detail'),
]
