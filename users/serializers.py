from rest_framework import serializers
from django.contrib.auth import get_user_model

Profile = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'password']
        extra_kwargs = {'username': {'write_only': True}, 'password': {'write_only': True}, 'email': {'write_only': True}}

    def create(self, validated_data):
        user = Profile.objects.create_user(**validated_data)
        user.save()
        return user
    