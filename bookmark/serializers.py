from rest_framework import serializers
from django.contrib.auth.models import User
from post.models import PerformancePost
from . import models


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bookmark  # User를 Bookmark로 변경합니다
        fields = ["username", "email", "date_joined"]  # 필요한 경우 필드 이름을 수정합니다


class PerformancePostBookmarkSerializer(
    serializers.ModelSerializer
):  # PerformancePostBookmarkSerializer 클래스를 정의하고, DRF의 ModelSerializer를 상속받습니다
    user = BookmarkSerializer(read_only=True)  # BookmarkSerializer를 사용하여 user 필드를 설명합니다

    class Meta:  # Meta 클래스를 이용해 Serializer의 메타 데이터를 세팅합니다
        model = models.Bookmark  # 연결할 모델은 Bookmark입니다
        fields = ["post", "user", "created_on"]  # Bookmark 모델의 필드들을 선택합니다

    def create(self, validated_data):  # 새북마크 인스턴스를 생성합니다
        request = self.context["request"]  # 요청객체를 가져옵니다
        ModelClass = self.Meta.model  # Bookmark 모델 클래스를 참조합니다

        instance = ModelClass.objects.create(  # Bookmark 인스턴스를 생성합니다
            **validated_data,
            **{"user": request.user}  # 인증된 데이터를 사용하고, user 필드는 요청의 사용자로 설정합니다
        )
        return instance
