import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .serializers import BookSerializer, PublisherBookSerializer
from common.exception_handlers import handle_unexpected_error
from .services.services import create_or_retrieve_authors, get_all_books, get_active_books, get_my_books
from common.pagination import CustomPageNumberPagination
from common.permissions import IsUploader

logger = logging.getLogger(__name__)

class BookView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get(self, request):
        try:
            books = get_active_books()
            paginator = self.pagination_class()
            paginated_books = paginator.paginate_queryset(books, request)
            serializer = BookSerializer(paginated_books, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        except Exception as err:
            return handle_unexpected_error(err, "An unexpected error occurred while retrieving books.")

    def post(self, request):
        try:
            author_names = request.data.pop('author', [])
            authors = create_or_retrieve_authors(author_names)

            serializer = BookSerializer(data=request.data, context={'user': request.user})
            if serializer.is_valid():
                serializer.save(author=authors, uploaded_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            logger.warning('BookView: invalid Book creation data: %s', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as err:
            return handle_unexpected_error(err, "An unexpected error occurred while uploading book.")
    
class SingleBookView(RetrieveAPIView):
    queryset = get_all_books()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

class PublisherMyBooksView(ListAPIView):
    serializer_class = PublisherBookSerializer
    permission_classes = [IsAuthenticated]
    pagination_class =  CustomPageNumberPagination

    def get_queryset(self):
        return get_my_books(self.request.user)

class PublisherSingleBookView(RetrieveUpdateDestroyAPIView):
    queryset = get_all_books()
    serializer_class = PublisherBookSerializer
    permission_classes = [IsAuthenticated, IsUploader]
    lookup_field = 'id'

class AdminAllBooksView(ListAPIView):
    queryset = get_all_books()
    serializer_class = PublisherBookSerializer
    permission_classes = [IsAdminUser]
    pagination_class =  CustomPageNumberPagination
