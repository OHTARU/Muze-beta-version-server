from rest_framework import serializers
from django.contrib.auth.models import User
from post.models import PerformancePost
from . import models


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "date_joined"]


class PerformancePostBookmarkSerializer(serializers.ModelSerializer):
    user = BookmarkSerializer(read_only=True)

    class Meta:
        model = models.Bookmark
        fields = ["post", "user", "created_on"]  # Bookmark 모델의 필드들을 선택합니다

    def create(self, validated_data):  # 새북마크 인스턴스를 생성합니다
        request = self.context["request"]  # 요청객체를 가져옵니다
        ModelClass = self.Meta.model  # Bookmark 모델 클래스를 참조합니다

        instance = ModelClass.objects.create(  # Bookmark 인스턴스를 생성합니다
            **validated_data,
            **{"user": request.user}  # 인증된 데이터를 사용하고, user 필드는 요청의 사용자로 설정합니다
        )
        return instance
