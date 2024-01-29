from rest_framework import serializers
from .models import Organisation, OrganisationInfo
from station.serializers import StationSerializer


class OrganisationSerializer(serializers.ModelSerializer):
  stations = serializers.SerializerMethodField()

  def get_stations(self, organisation):
    return ', '.join([str(station) for station in organisation.station.all()])
  
  class Meta:
    model = Organisation
    fields = ['id', 'short_name', 'stations', 'slogan']

class OrganisationInfoSerializer(serializers.ModelSerializer):
  organisation = OrganisationSerializer()
  station = StationSerializer()
  
  class Meta:
    model = OrganisationInfo
    fields = ['id', 'meeting_days', 'meeting_days_suff', 'meeting_frequency', 'meeting_info', 'organisation', 'station']
