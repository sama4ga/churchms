from rest_framework import serializers
from .models import Station

class StationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Station
    fields = ['id', 'name', 'address', 'date_created', 'picture']