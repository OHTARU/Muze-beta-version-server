from django.contrib import admin
from .models import Bookmark


class bookmarkAdmin(admin.ModelAdmin):
    list_per_page = 10


admin.site.register(Bookmark, bookmarkAdmin)
