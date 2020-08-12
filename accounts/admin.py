from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'furigana', 'email', 'tel')

admin.site.register(CustomUser, CustomUserAdmin)