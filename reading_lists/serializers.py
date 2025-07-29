from django.http import Http404
from rest_framework import serializers
from .models import ReadingList, ReadingListBook
from .services.db_service import does_similar_reading_list_exists, does_reading_list_belongs_to_the_user, does_similar_reading_list_book_exists, is_book_active
from common.base_db_service import get_object_or_404_by_pk

class ReadingListBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingListBook
        fields = "__all__"
        read_only_fields = ["id", "order"]

    def validate(self, attrs):
        user = self.context.get("user")
        reading_list = attrs.get("reading_list")
        book = attrs.get("book")
        if not does_reading_list_belongs_to_the_user(user, reading_list):
            raise serializers.ValidationError({"reading_list": "You don't have the pemission to this reading list"})
        if not is_book_active(book):
            raise serializers.ValidationError({"book": "The book is not available now"})
        if does_similar_reading_list_book_exists(reading_list, book):
            raise serializers.ValidationError({"book": "You already have this book in the reading list"})
        return attrs
    
class ReadingListSerializer(serializers.ModelSerializer):
    total_books = serializers.SerializerMethodField()
    class Meta:
        model = ReadingList
        exclude = ["user"]
        read_only_fields = ["id", "created_at", "updated_at"]
    
    def get_total_books(self, obj):
        return obj.books_list.count()

    def validate(self, attrs):
        user = self.context['request'].user
        name = attrs.get('name')
        if len(name) < 3:
            raise serializers.ValidationError('name must be at least 3 characters long.')
        if user and name:
            if does_similar_reading_list_exists(user, name):
                raise serializers.ValidationError({"name": "You already have a reading list with this name."})
        return attrs

class DetailedReadingListSerializer(serializers.ModelSerializer):
    books_list = ReadingListBookSerializer(many=True)
    class Meta:
        model = ReadingList
        exclude = ["user"]
        read_only_fields = ["id", "created_at", "updated_at", "books_list"]

class ReorderReadingListBookSerializer(serializers.Serializer):
    new_order = serializers.IntegerField(min_value=1)

    def validate(self, data):
        reading_list_book_id = self.context.get('reading_list_book_id')
        new_order = data.get('new_order')
        try:
            reading_list_book = get_object_or_404_by_pk(ReadingListBook, reading_list_book_id)
        except Http404:
            raise serializers.ValidationError("Reading list item does not exist")
 
        reading_list = reading_list_book.reading_list
        max_order = reading_list.books_list.count()
        if new_order > max_order:
            raise serializers.ValidationError(f"Updating order cannot be greater than {max_order}.")
        
        if new_order == reading_list_book.order:
            raise serializers.ValidationError(f"Updating order cannot be the same as existing order.")
        
        data['reading_list_book'] = reading_list_book
        data['max_order'] = max_order
        return data