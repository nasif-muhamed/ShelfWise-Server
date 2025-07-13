from django.db import models
from django.contrib.auth import get_user_model

Profile = get_user_model()

class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ManyToManyField(Author, related_name='books')
    genre = models.CharField(max_length=100)
    publication_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    uploaded_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='uploaded_books')
    cover = models.ImageField(upload_to='book/images', null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-publication_date']
        constraints = [
            models.UniqueConstraint(fields=['uploaded_by', 'title'], name='unique_book_per_uploader')
        ]

    def __str__(self):
        return self.title
