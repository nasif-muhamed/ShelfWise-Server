from django.db.models import F
from ..models import ReadingList

def does_similar_reading_list_exists(user, title):
    return ReadingList.objects.filter(user=user, name=title).exists()

def get_my_reading_lists(user):
    return user.reading_lists.all()

def does_reading_list_belongs_to_the_user(user, reading_list):
    return reading_list.user == user

def does_book_belongs_to_reading_list(reading_list_book, reading_list_id):
    return reading_list_book.reading_list_id == reading_list_id

def does_similar_reading_list_book_exists(reading_list, book):
    return reading_list.books_list.filter(book=book).exists()

def is_book_active(book):
    return book.is_active

def rotate_reading_list_order_by_adding(reading_list, start, end=None):
    if end is None:
        end = reading_list.books_list.count()
    to_rotate_list = reading_list.books_list.filter(order__gte=start, order__lte=end)
    rotated_list = to_rotate_list.update(order=F('order') + 1)
    return rotated_list

def delete_reading_list_book_instance(reading_list_book):
    reading_list_book.delete()

def rotate_reading_list_order_by_deducting(reading_list, start, end=None):
    if end is None:
        end = reading_list.books_list.count()
    to_update_list = reading_list.books_list.filter(order__gt=start, order__lte=end)
    updated_list = to_update_list.update(order=F('order') - 1)
    return updated_list
