from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['username', 'email']
    date_hierarchy = 'created_at'

    fieldsets = UserAdmin.fieldsets + (
        ('额外信息', {'fields': ('avatar_url', 'bio')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('额外信息', {'fields': ('avatar_url', 'bio')}),
    )