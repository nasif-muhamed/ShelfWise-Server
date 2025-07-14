from django.db.models.functions import Lower
from ..models import Author, Book

# Author
def get_create_author(author_name):
    author, _ = Author.objects.get_or_create(name=author_name)
    return author

# Book
def does_similar_book_exists(title):
    return Book.objects.annotate(lower_title=Lower('title')).filter(lower_title=title.lower()).exists()