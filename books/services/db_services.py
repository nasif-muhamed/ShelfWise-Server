from ..models import Author, Book

# Author
def get_create_author(author_name):
    author, _ = Author.objects.get_or_create(name=author_name)
    return author

# Book
def does_similar_book_exists(user, title):
    return Book.objects.filter(uploaded_by=user, title=title).exists()