from rest_framework import serializers
from .models import WorkingSociety
from organisation.serializers import OrganisationInfoSerializer

class WorkingSocietySerializer(serializers.ModelSerializer):
  organisation = OrganisationInfoSerializer()
  class Meta:
    model = WorkingSociety
    fields = ['id', 'name', 'organisation']