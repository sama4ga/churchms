from rest_framework import serializers
from .models import Parishioner, DeathDetail
from station.serializers import StationSerializer
from organisation.serializers import OrganisationInfoSerializer
from society.serializers import WorkingSocietySerializer
from other_group.serializers import OtherGroupInfoSerializer
from pious_society.serializers import PiousSocietyInfoSerializer
from lay_apostolate.serializers import LayApostolateInfoSerializer
from users.serializers import UserSerializer

class DeathDetailSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = DeathDetail
    fields = ['id', 'parishioner', 'died_on', 'buried_on', 'buried_by', 'buried_at']

class ParishionerSerializer(serializers.ModelSerializer):
  station = StationSerializer()
  organisation = OrganisationInfoSerializer()
  working_society = WorkingSocietySerializer()
  othergroupinfo_set = OtherGroupInfoSerializer(many=True)
  pioussocietyinfo_set = PiousSocietyInfoSerializer(many=True)
  layapostolateinfo_set = LayApostolateInfoSerializer(many=True)
  created_by = UserSerializer()
  modified_by = UserSerializer()
  deleted_by = UserSerializer()
  
  class Meta:
    model = Parishioner
    # fields = '__all__'
    fields = ['id', 'title', 'surname', 'first_name', 'middle_name', 'fullname', 'phone_number', 'occupation', 'residential_address', 'home_address', 'office_address', 'diocese_of_origin', 'parish_of_origin', 'state_of_origin', 'lga_of_origin', 'email', 'passport', 'marital_status', 'gender', 'date_of_birth', 'spouse_name', 'baptised', 'communicant', 'status', 'confirmed', 'wedded', 'charisma', 'station', 'station_status', 'organisation', 'organisation_status', 'working_society', 'working_society_status', 'pioussocietyinfo_set', 'othergroupinfo_set', 'layapostolateinfo_set', 'created_by', 'created_on', 'modified_by', 'modified_on', 'deleted_by', 'deleted_on', 'death_detail']
    depth = 1
