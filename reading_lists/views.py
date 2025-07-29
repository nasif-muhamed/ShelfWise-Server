import logging
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ValidationError
from .serializers import ReadingListSerializer, ReadingListBookSerializer, DetailedReadingListSerializer, ReorderReadingListBookSerializer
from .services.services import get_my_reading_list, delete_and_update_reading_list_book, update_and_reorder_reading_list_books, reorder_reading_list
from common.exception_handlers import handle_unexpected_error
from common.permissions import IsReadingListOwner
from common.pagination import CustomPageNumberPagination

logger = logging.getLogger(__name__)

class ReadingListViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        return get_my_reading_list(self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailedReadingListSerializer
        return ReadingListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReadingListBookView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            serializer = ReadingListBookSerializer(data=request.data, context={'user': request.user})
            if serializer.is_valid():
                reading_list = serializer.validated_data["reading_list"]
                updated_readinglist = reorder_reading_list(reading_list, pos=1)
                serializer.save(order=1)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            error = {"detail": "reading list or book with the id doesn't exist."}
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            return handle_unexpected_error(err, "An unexpected error occured while adding book to reading list.")

class SingleReadingListBookView(APIView):
    permission_classes = [IsAuthenticated, IsReadingListOwner]
    def patch(self, request, reading_list_book_id):
        context={'reading_list_book_id': reading_list_book_id}
        serializer = ReorderReadingListBookSerializer(data=request.data, context=context)
        if serializer.is_valid():
            reading_list_book = serializer.validated_data['reading_list_book']
            new_order = serializer.validated_data['new_order']
            rotated_reading_list, updated_reading_list_book = update_and_reorder_reading_list_books(reading_list_book, new_order)
            serializer = ReadingListBookSerializer(updated_reading_list_book)
            logger.debug(f"result update_and_reorder_reading_list_books: {rotated_reading_list}, {updated_reading_list_book}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.warning("SingleReadingListBookView PATCH: Invalid reorder data: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def delete(self, request, reading_list_book_id):
        try:
            user = request.user
            delete_and_update_reading_list_book(id=reading_list_book_id, user=user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as err:
            raise
        except Exception as err:
            return handle_unexpected_error(err, "An unexpected error occured while deleting book from reading list.")
        
