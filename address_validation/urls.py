#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
        path('', views.AddressListCreateView.as_view(), name='address-list-create'),
        path('validate-address/', views.ValidateAddressView.as_view(), name='validate-address'),
]
