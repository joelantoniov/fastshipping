#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
        path('status/', views.PackageStatusListCreateView.as_view(), name='package-status-list-create'),
        path('status/<int:pk>', views.PackageStatusDetailView.as_view(), name='package-status-detail'),
]
