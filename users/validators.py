import re
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db.models.functions import Lower

Profile = get_user_model()
USERNAME_PATTERN = r'^[a-z_]+$'
USERNAME_CONTAINS = r'[a-zA-Z]'
NAME_PATTERN = r'^[a-zA-Z]+([ \'-][a-zA-Z]+)*$'
BIO_PATTERN = r'^[a-zA-Z0-9\s.,\'-]*$'

def validate_username(value):
    if len(value) < 4:
        raise ValidationError("Username must be at least 4 characters long.")
    if len(value) > 20:
        raise ValidationError("Username cannot be longer than 20 characters.")

    if len(re.findall(USERNAME_CONTAINS, value)) < 3:
        raise ValidationError("Username must contain at least three alphabetic characters.")
    
    if not re.match(USERNAME_PATTERN, value):
        raise ValidationError("Username must only contain lowercase letters and underscores, with no spaces.")
    
    if Profile.objects.filter(username__iexact=value.lower()).exists():
        raise ValidationError("This username is already taken.")
    
    return value

def validate_first_name(value):
    if len(value) < 3:
        raise ValidationError("First Name must be at least 3 characters long.")
    if len(value) > 50:
        raise ValidationError("First Name cannot be longer than 50 characters.")

    if not re.match(NAME_PATTERN, value):
        raise ValidationError("Name must only contain alphabetic characters, spaces, apostrophes, or hyphens.")

    return value

def validate_last_name(value):
    if len(value) < 1:
        raise ValidationError("Last name must be at least 1 characters long.")
    if len(value) > 50:
        raise ValidationError("Last name cannot be longer than 50 characters.")

    if not re.match(NAME_PATTERN, value):
        raise ValidationError("Name must only contain alphabetic characters, spaces, apostrophes, or hyphens.")

    return value

def validate_bio(value):
    if len(value) < 10:
        raise ValidationError("Bio must be at least 10 characters long.")
    if len(value) > 250:
        raise ValidationError("Bio name cannot be longer than 250 characters.")
    
    if not re.match(BIO_PATTERN, value):
        raise ValidationError("Bio can only contain letters, numbers, spaces, and common punctuation (.,'-).")

    return value
