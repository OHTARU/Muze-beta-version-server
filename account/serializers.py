from rest_framework import serializers
from .models import UserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            "id",
            "name",
            "profile",
            "type",
            "create_at",
            "is_admin",
            "is_active",
            "is_staff",
            "is_superuser",
        ]
        # fields = "__all__"
