from django.contrib.auth import get_user_model

Profile = get_user_model()

def create_user(**attrs):
    user = Profile.objects.create_user(**attrs)
    return user