from .models import PerformancePost
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PerformancePost
        fields = "__all__"
        # ('Age','Educations','Career','Award','Introduce','Created','Updated')
