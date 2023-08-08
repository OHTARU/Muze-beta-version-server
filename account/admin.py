from django.contrib import admin
from .models import UserModel


class UserAdmin(admin.ModelAdmin):
    list_per_page = 10


admin.site.register(UserModel, UserAdmin)
