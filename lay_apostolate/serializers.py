from rest_framework import serializers
from .models import LayApostolate
from parishioner.models import LayApostolateInfo

class LayApostolateSerializer(serializers.ModelSerializer):
  class Meta:
    model = LayApostolate
    fields = ('id', 'name', 'short_name', 'slogan', 'status')  
    
class LayApostolateInfoSerializer(serializers.ModelSerializer):
  lay_apostolate = LayApostolateSerializer()
  # parishioner = serializers.CharField()
  
  class Meta:
    model = LayApostolateInfo
    fields = ('id', 'parishioner', 'lay_apostolate', 'status')
