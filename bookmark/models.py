from django.db import models
from django.conf import settings
from post.models import PerformancePost
from django.utils import timezone


class Bookmark(models.Model):
    user = models.ForeignKey(  # user와 Bookmark 간의 연결
        settings.AUTH_USER_MODEL,  # 인증된 사용자 모델을 참조
        on_delete=models.CASCADE,  # 사용자가 삭제되면 관련 북마크도 삭제
        related_name="bookmark",  # 사용자가 북마크한 항목에 쉽게 접근
    )

    post = models.ForeignKey(  # post와 Bookmark 간의 연결
        PerformancePost,
        on_delete=models.CASCADE,  # 게시물이 삭제되면 관련 북마크도 삭제
        related_name="bookmarked",  # 게시물과 관련된 모든 북마크에 접근
    )

    # 북마크 생성 시간 저장
    # 기본값으로 timezone.now를 사용하여 현재 시각이 자동으로 저장
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user}님이 {self.post} 게시물을 즐겨찾기했습니다."
