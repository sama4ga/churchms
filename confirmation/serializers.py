from rest_framework import serializers
from .models import Confirmation

class ConfirmationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Confirmation
    fields = ('id', 'candidate', 'minister', 'sponsor', 'date')
    depth = 1

class ConfirmationSerializer1(serializers.ModelSerializer):
  candidate = serializers.HyperlinkedRelatedField(view_name='parishioner-detail', read_only=True, format='html')
  candidate_name = serializers.CharField(source='candidate')
  class Meta:
    model = Confirmation
    fields = ('id', 'candidate', 'candidate_name', 'minister', 'sponsor', 'date')
    depth = 1