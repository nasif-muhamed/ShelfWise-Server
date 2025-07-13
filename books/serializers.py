from rest_framework import serializers
from .models import Book, Author
from users.serializers import ProfileSerializer
from .services.db_services import does_similar_book_exists

class BookSerializer(serializers.ModelSerializer):
    uploaded_by = ProfileSerializer(read_only=True)
    author = serializers.SerializerMethodField()

    class Meta:
        model = Book
        exclude = ["is_active"]
        read_only_fields = ["id", "publication_date", "author", "uploaded_by"]

    def validate(self, attrs):
        user = self.context.get('user')
        title = attrs.get('title')
        if user and title:
            if does_similar_book_exists(user, title):
                raise serializers.ValidationError({"title": "You have already uploaded a book with this title."})

        return attrs
    
    def get_author(self, obj):
        return [author.name for author in obj.author.all()]

class PublisherBookSerializer(serializers.ModelSerializer):
    uploaded_by = ProfileSerializer(read_only=True)
    author = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ["id", "publication_date", "author", "uploaded_by"]

    def validate(self, attrs):
        user = self.context.get('user')
        title = attrs.get('title')
        if user and title:
            if does_similar_book_exists(user=user, title=title):
                raise serializers.ValidationError({"title": "You have already uploaded a book with this title."})

        return attrs
    
    def get_author(self, obj):
        return [author.name for author in obj.author.all()]
