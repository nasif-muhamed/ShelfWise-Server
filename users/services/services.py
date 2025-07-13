from common.base_db_service import get_obj_with_pk, update_model_attrs, get_all_objects
from django.contrib.auth import get_user_model
from .db_services import create_user

Profile = get_user_model()

def take_user_action(pk, is_active):
    user = get_obj_with_pk(Profile, pk=pk)
    updated_user = update_model_attrs(instance=user, is_active=is_active)
    updated_user.save()
    return updated_user
    
def get_all_profiles():
    return get_all_objects(Profile)

def create_new_user(data):
    user = create_user(**data)
    user.save()
    return user