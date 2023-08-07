from django.contrib import admin
from .models import PerformancePost


class PerformancePostAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        "id",
        "author",
        "title",
        "call",
        "agency",
        "type",
        "deadline",
        "date",
    )


admin.site.register(PerformancePost, PerformancePostAdmin)
