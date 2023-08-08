from datetime import datetime
from django.db import models
from config import settings

## Resume == consumer


class Resume(models.Model):
    id = models.AutoField(primary_key=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="consum_user"
    )  # 작성자
    call = models.CharField(max_length=254)  # 연락처
    gender = models.CharField(max_length=50, default="무관")  # 성별
    profile = models.ImageField(upload_to="media/Resume", null=True, blank=True)

    age = models.PositiveIntegerField(blank=False, null=False, default=17)  # 나이

    education = models.CharField(max_length=254)  # 학력

    career = models.CharField(max_length=254)  # 경력

    award = models.CharField(max_length=254)  # 수상수력

    introduce = models.CharField(max_length=254)  # 자기소개서

    created = models.DateTimeField(default=datetime.now)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author}님이 작성한 게시물입니다."
