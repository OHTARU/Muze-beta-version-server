from .models import Resume
from rest_framework import serializers


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = "__all__"
        # ('Age','Educations','Career','Award','Introduce','Created','Updated')
