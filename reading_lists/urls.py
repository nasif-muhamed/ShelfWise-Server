from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ReadingListViewSet, ReadingListBookView, SingleReadingListBookView

router = DefaultRouter()
router.register(r'', ReadingListViewSet, basename='readinglist')

urlpatterns = [
    path(r'reading-lists/', include(router.urls)),
    path('reading-list-book/', ReadingListBookView.as_view(), name="reading-list-book"),
    path('reading-list-book/<int:reading_list_book_id>/', SingleReadingListBookView.as_view(), name="reading-list-book"),
]
