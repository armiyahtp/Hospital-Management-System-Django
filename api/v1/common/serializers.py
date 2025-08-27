from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


from django.contrib.auth import get_user_model




User = get_user_model()

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'phone_number', 'first_name', 'last_name')
        read_only_fields = ('id',)







class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name',  'last_name', 'phone_number', 'password', 'confirm_password',)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return data