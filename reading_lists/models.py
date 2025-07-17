from django.db import models
from django.contrib.auth import get_user_model
from books.models import Book

Profile = get_user_model()

class ReadingList(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(Profile, related_name="reading_lists", on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(fields=['name', 'user'], name='unique_read_list_per_uploader')
        ]

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class ReadingListBook(models.Model):
    reading_list = models.ForeignKey(ReadingList, related_name="books_list", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ('reading_list', 'book')
        ordering = ['order']

    def __str__(self):
        return f"{self.book.title} in {self.reading_list.name} (Order: {self.order})"
