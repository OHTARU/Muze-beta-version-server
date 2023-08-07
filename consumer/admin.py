from django.contrib import admin
from .models import Resume


class ResumeAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ("id", "author", "call", "age", "created", "updated")


admin.site.register(Resume, ResumeAdmin)
