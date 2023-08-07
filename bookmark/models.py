from django.db import models
from django.conf import settings
from post.models import PerformancePost
from django.utils import timezone


class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookmark",
        null=True,  # Allow null values for the ForeignKey field
        default=None,
    )
    post = models.ForeignKey(
        PerformancePost,
        on_delete=models.CASCADE,
        related_name="bookmarked",
        null=True,  # Allow null values for the ForeignKey field
        default=None,
    )
    created_on = models.DateTimeField(default=timezone.now)
