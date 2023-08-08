from django.contrib import admin
from .models import Resume


class ResumeAdmin(admin.ModelAdmin):
    list_per_page = 10


admin.site.register(Resume, ResumeAdmin)
