from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ["user_permissions", "groups"]
    readonly_fields = [
        "password",
        "last_login",
        "is_superuser",
        "is_staff",
        "is_active",
        "email",
    ]
    list_display = ["email", "id", "role", "is_active"]
    list_filter = ["role"]
    search_fields = ["email", "last_name"]
