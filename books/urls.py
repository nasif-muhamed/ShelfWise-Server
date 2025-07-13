from django.urls import path
from .views import BookView, SingleBookView, PublisherSingleBookView, PublisherMyBooksView, AdminAllBooksView \

urlpatterns = [
    path('', BookView.as_view(), name='books-crud'),
    path('<int:id>/', SingleBookView.as_view(), name='sigle-book-public-view'),
    path('my-books/', PublisherMyBooksView.as_view(), name='sigle-book-publisher-crud'),
    path('publisher/<int:id>/', PublisherSingleBookView.as_view(), name='sigle-book-publisher-crud'),
    path('admin/all-books/', AdminAllBooksView.as_view(), name='admin-all-books'),
]
