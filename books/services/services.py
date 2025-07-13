from .db_services import get_create_author
from ..models import Book
from common.base_db_service import get_all_objects, get_filtered_objects

def create_or_retrieve_authors(author_names):
    authors = []
    for author_name in author_names:
        author = get_create_author(author_name)
        authors.append(author)
    return authors

def get_all_books():
    return get_all_objects(model_class=Book)

def get_active_books():
    return get_filtered_objects(model_class=Book, filters={"is_active": True})

def get_my_books(user):
    return get_filtered_objects(model_class=Book, filters={"uploaded_by": user})