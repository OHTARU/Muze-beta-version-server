from django.urls import path
from .views import BookmarkListCreateView, BookmarkDeleteView

urlpatterns = [
    path("", BookmarkListCreateView.as_view(), name="bookmark_list_create"),
    path("<int:id>/", BookmarkDeleteView.as_view(), name="bookmark_delete"),
]
