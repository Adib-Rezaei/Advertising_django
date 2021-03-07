from rest_framework import serializers
from .models import AdvertiserModel, AdModel, ClickModel, ViewModel


class AdvertiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertiserModel
        fields = ['id', 'name']


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdModel
        fields = ['id', 'advertiser', 'title', 'link', 'approved']

