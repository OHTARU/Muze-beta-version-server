from django.urls import path
from .views import PostDetail, PostList

urlpatterns = [
    path("", PostList.as_view(), name="post-list"),
    path("<int:pk>/", PostDetail.as_view(), name="post-detail"),
    path("delete/<int:pk>/", PostDetail.as_view(), name="post_delete"),
]
