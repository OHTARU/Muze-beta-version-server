# posts/models.py
# 공연정보 게시판

from django.db import models
from datetime import datetime
from config import settings


class PerformancePost(models.Model):
    id = models.AutoField(primary_key=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="Post_author"
    )  # 작성자
    gender = models.CharField(max_length=50, default="무관")  # 성별
    agency = models.CharField(max_length=50, null=False, default="기관명")  # 주최기관
    title = models.CharField(max_length=200)  # 포스트 제목
    call = models.CharField(max_length=50)  # 연락수단
    pay = models.CharField(
        max_length=50,
        null=True,
        default="0",
    )  #
    info = models.TextField()  # 공연정보
    type = models.CharField(max_length=50)  # 공연종류
    deadline = models.CharField(max_length=50)  # 모집기한
    date = models.CharField(max_length=50)  # 공연일시
    location = models.CharField(max_length=300)  # 공연장소
    profile = models.ImageField(upload_to="media/Post", null=True, blank=True)  # 포스터사진

    Created = models.DateTimeField(default=datetime.now)
    Updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
