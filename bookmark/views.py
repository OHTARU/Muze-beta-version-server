from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Bookmark
from .serializers import BookmarkSerializer


class BookmarkListCreateView(generics.ListCreateAPIView):
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        user = self.request.user
        return Bookmark.objects.filter(user=user)


class BookmarkDeleteView(generics.DestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        bookmark_id = kwargs["id"]

        if user.is_authenticated:
            bookmark = get_object_or_404(Bookmark, id=bookmark_id)
            if bookmark.user == user:
                bookmark.delete()
                return Response(
                    {"detail": "Bookmark deleted."}, status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {"detail": "Not authorized to delete this bookmark."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        else:
            return Response(
                {"detail": "User not authenticated."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
