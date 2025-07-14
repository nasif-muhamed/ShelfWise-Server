from django.http import Http404
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .base_db_service import get_object_or_404_by_pk
from reading_lists.models import ReadingListBook
from reading_lists.services.db_service import does_reading_list_belongs_to_the_user

class IsUploader(BasePermission):
    """
    Custom permission to check if the book is uploaded by the user.
    """
    def has_object_permission(self, request, view, obj):
        return obj.uploaded_by == request.user

class IsReadingListOwner(BasePermission):
    """
    Custom permission to check if the user owns the ReadingList.
    """
    def has_permission(self, request, view):
        reading_list_book_id = view.kwargs.get('reading_list_book_id')
        try:
            reading_list_book = get_object_or_404_by_pk(ReadingListBook, reading_list_book_id)
            return does_reading_list_belongs_to_the_user(request.user, reading_list_book.reading_list)
        except Http404:
            return False