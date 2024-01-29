from rest_framework import serializers
from .models import Matrimony

class MatrimonySerializer(serializers.ModelSerializer):
  class Meta:
    model = Matrimony
    fields = ('id', 'bride', 'bride_parent', 'bride_village', 'groom', 'groom_parent', 'groom_village', 'sponsor', 'sponsor_address', 'minister', 'date')
    depth = 1

class MatrimonySerializer1(serializers.ModelSerializer):
  bride = serializers.HyperlinkedRelatedField(view_name='parishioner-detail', read_only=True, format='html')
  bride_name = serializers.CharField(source='bride')
  groom = serializers.HyperlinkedRelatedField(view_name='parishioner-detail', read_only=True, format='html')
  groom_name = serializers.CharField(source='groom')
  minister = serializers.HyperlinkedRelatedField(view_name='priest-detail', read_only=True, format='html')
  minister_name = serializers.CharField(source='minister')
  class Meta:
    model = Matrimony
    fields = ('id', 'bride', 'bride_name', 'bride_parent', 'bride_village', 'groom', 'groom_name', 'groom_parent', 'groom_village', 'sponsor', 'sponsor_address', 'minister', 'minister_name', 'date')
    depth = 1