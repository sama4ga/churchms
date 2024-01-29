from rest_framework import serializers
from .models import PiousSociety
from parishioner.models import PiousSocietyInfo

class PiousSocietySerializer(serializers.ModelSerializer):
  class Meta:
    model = PiousSociety
    fields = ('id', 'name', 'slogan', 'status')
    
class PiousSocietyInfoSerializer(serializers.ModelSerializer):
  pious_society = PiousSocietySerializer()
  # parishioner = serializers.CharField()
  
  class Meta:
    model = PiousSocietyInfo
    fields = ('id', 'parishioner', 'pious_society', 'status')

    