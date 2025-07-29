import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .services.services import create_new_user
from .validators import validate_username, validate_first_name, validate_last_name, validate_bio

Profile = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[validate_username])
    class Meta:
        model = Profile
        fields = ['username', 'email', 'password']
        extra_kwargs = {'username': {'write_only': True}, 'password': {'write_only': True}, 'email': {'write_only': True}}

    def validate_username(self, value):
        if len(value) < 4:
            raise serializers.ValidationError('Username must be at least 4 characters long.')
        return value
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long.')            
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError('Password must contain at least one special character.')
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError('Password must contain at least one digit.')
        if re.search(r'\s', value):
            raise serializers.ValidationError('Password must not contain empty space.')
        return value            

    def create(self, validated_data):
        user = create_new_user(validated_data)
        return user
    
class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['password', 'user_permissions', 'groups', "date_joined", "last_login"]

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(validators=[validate_first_name], required=False)
    last_name = serializers.CharField(validators=[validate_last_name], required=False)
    bio = serializers.CharField(validators=[validate_bio], required=False)
    class Meta:
        model = Profile
        fields = ["id", "username", "first_name", "last_name", "email", "bio", "picture", "created_at"]
        read_only_fields = ["id", "created_at", "username", "email"]

    def validate(self, attrs):
        first_name = attrs.get("first_name", None)
        last_name = attrs.get("last_name", None)
        bio = attrs.get("bio", None)
        if first_name and len(first_name) < 3:
            raise serializers.ValidationError('First name should contain at least 3 characters')
        if last_name and len(last_name) < 3:
            raise serializers.ValidationError('Last name should contain at least 3 characters')
        if bio and len(bio) < 10:
            raise serializers.ValidationError('Biography should contain at least 10 characters')
        return attrs

# using in Books serializers for retrieving user details
class ProfileSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Profile
        fields = ['id', 'username', 'first_name', 'last_name', 'bio', 'picture']
        read_only_fields = ['id', 'username', 'first_name', 'last_name', 'bio', 'picture']
