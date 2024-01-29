from rest_framework import serializers
from .models import OtherGroup
from parishioner.models import OtherGroupInfo

class OtherGroupSerializer(serializers.ModelSerializer):
  class Meta:
    model = OtherGroup
    fields = ('id', 'name', 'short_name', 'slogan','status')  
    
class OtherGroupInfoSerializer(serializers.ModelSerializer):
  other_group = OtherGroupSerializer()
  # parishioner = serializers.CharField()
  
  class Meta:
    model = OtherGroupInfo
    fields = ('id', 'parishioner', 'other_group', 'status')
