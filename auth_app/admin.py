from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'date_created')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_created')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_created',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('date_created',)}),
    )
    readonly_fields = ('date_created',)
