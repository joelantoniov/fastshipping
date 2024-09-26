#! /usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import PackageStatus

class PackageStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageStatus
        fields = '__all__'
