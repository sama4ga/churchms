from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'email')
    # fields = ('id', 'username', 'email', 'password', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions', 'last_login', 'date_joined', 'first_name', 'last_name')
    # depth = 1