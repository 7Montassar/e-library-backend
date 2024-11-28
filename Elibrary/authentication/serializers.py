from rest_framework import serializers
from .models import User
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
       model = User
       fields = ('id', 'username', 'full_name', 'password', 'role')
       extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
       user = User.objects.create_user(
           username=validated_data['username'],
           full_name=validated_data['full_name'],
           password=validated_data['password']
       )
       return user