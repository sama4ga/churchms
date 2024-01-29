from rest_framework import serializers
from .models import Communion

class CommunionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Communion
    fields = ('id', 'candidate', 'minister', 'sponsor', 'date')
    depth = 1

class CommunionSerializer1(serializers.ModelSerializer):
  candidate = serializers.HyperlinkedRelatedField(view_name='parishioner-detail', read_only=True, format='html')
  candidate_name = serializers.CharField(source='candidate')
  minister = serializers.HyperlinkedRelatedField(view_name='priest-detail', read_only=True, format='html')
  minister_name = serializers.CharField(source='minister')
  class Meta:
    model = Communion
    fields = ('id', 'candidate', 'candidate_name', 'minister', 'minister_name', 'sponsor', 'date')
    depth = 1