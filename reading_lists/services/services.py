from django.db import transaction
from rest_framework.serializers import ValidationError
from .db_service import get_my_reading_lists, delete_reading_list_book_instance, rotate_reading_list_order_by_deducting, \
    does_book_belongs_to_reading_list, rotate_reading_list_order_by_adding
from common.base_db_service import get_object_or_404_by_pk, update_instance_attributes
from ..models import ReadingListBook

def get_my_reading_list(user):
    return get_my_reading_lists(user)

def reorder_reading_list(reading_list, pos):
    updated_list = rotate_reading_list_order_by_adding(reading_list, pos)
    return updated_list

@transaction.atomic
def delete_and_update_reading_list_book(id, user):
    reading_list_book = get_object_or_404_by_pk(ReadingListBook, id)
    reading_list = reading_list_book.reading_list
    current_order = reading_list_book.order
    delete_reading_list_book_instance(reading_list_book)
    rotate_reading_list_order_by_deducting(reading_list, current_order)
    return True

def update_and_reorder_reading_list_books(reading_list_book, new_order):
    with transaction.atomic():
        current_order = reading_list_book.order
        if current_order > new_order:
            rotated_reading_list = rotate_reading_list_order_by_adding(reading_list_book.reading_list, new_order, current_order)
        else:
            rotated_reading_list = rotate_reading_list_order_by_deducting(reading_list_book.reading_list, current_order, new_order)
        updated_reading_list_book = update_instance_attributes(reading_list_book, order=new_order)
        updated_reading_list_book.save()

    return rotated_reading_list, updated_reading_list_book