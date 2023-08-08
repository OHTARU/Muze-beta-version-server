from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Bookmark
from .serializers import BookmarkSerializer


# 북마크를 가져오거나 생성하는 API 뷰를 정의합니다 (ListCreateAPIView 이용)
class BookmarkListCreateView(generics.ListCreateAPIView):
    serializer_class = BookmarkSerializer

    # 현재 사용자와 연결된 북마크를 가져오는 쿼리셋을 정의합니다.
    def get_queryset(self):
        user = self.request.user
        return Bookmark.objects.filter(user=user)


# 북마크를 삭제하는 API 뷰를 정의합니다 (DestroyAPIView 이용)
class BookmarkDeleteView(generics.DestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    lookup_field = "id"

    # 삭제 요청을 처리하는 메서드를 정의합니다.
    def delete(self, request, *args, **kwargs):
        user = self.request.user
        bookmark_id = kwargs["id"]

        # 인증된 사용자인 경우
        if user.is_authenticated:
            bookmark = get_object_or_404(Bookmark, id=bookmark_id)

            # 사용자가 북마크의 소유자인 경우 삭제하고 결과 반환
            if bookmark.user == user:
                bookmark.delete()
                return Response(
                    {"detail": "즐겨찾기 삭제됨"}, status=status.HTTP_204_NO_CONTENT
                )
            # 소유자가 아닌 경우 권한 없음 오류 반환
            else:
                return Response(
                    {"detail": "삭제할 권한이 없습니다."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        # 인증되지 않은 사용자인 경우 오류 반환
        else:
            return Response(
                {"detail": "사용자가 인증되지 않았습니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
