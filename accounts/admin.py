"""
Custom User Admin
"""

import logging
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from .models import User
from .forms import UserCreationForm, UserChangeForm

logger = logging.getLogger("accounts")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for the custom User model."""

    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    # ---- List View ----
    list_display = (
        "email",
        "get_display_name",
        "get_full_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
        "avatar_preview",
    )
    list_display_links = ("email", "get_display_name")
    list_filter = ("is_active", "is_staff", "is_superuser", "date_joined")
    list_per_page = 25
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("-date_joined",)
    date_hierarchy = "date_joined"

    # ---- Actions ----
    actions = ["activate_users", "deactivate_users"]

    # ---- Detail View Fieldsets ----
    fieldsets = (
        (None, {
            "fields": ("email", "password"),
        }),
        (_("Personal Info"), {
            "fields": ("username", "first_name", "last_name", "avatar"),
        }),
        (_("Permissions"), {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
            "classes": ("collapse",),
        }),
        (_("Important Dates"), {
            "fields": ("last_login", "date_joined"),
            "classes": ("collapse",),
        }),
    )

    # ---- Add User Fieldsets ----
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "username",
                "first_name",
                "last_name",
                "password1",
                "password2",
                "is_active",
                "is_staff",
            ),
        }),
    )

    readonly_fields = ("last_login", "date_joined")

    # ---- Custom Display Methods ----
    @admin.display(description=_("Avatar"))
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;" />',
                obj.avatar.url,
            )
        return format_html('<span style="color:#ccc;">—</span>')

    @admin.display(description=_("Display Name"))
    def get_display_name(self, obj):
        return obj.get_display_name()

    @admin.display(description=_("Full Name"))
    def get_full_name(self, obj):
        return obj.get_full_name()

    # ---- Custom Actions ----
    @admin.action(description=_("Activate selected users"))
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        logger.info("Admin '%s' activated %d users.", request.user, updated)
        self.message_user(request, f"{updated} user(s) have been activated.")

    @admin.action(description=_("Deactivate selected users"))
    def deactivate_users(self, request, queryset):
        # Prevent deactivating yourself
        queryset = queryset.exclude(pk=request.user.pk)
        updated = queryset.update(is_active=False)
        logger.warning("Admin '%s' deactivated %d users.", request.user, updated)
        self.message_user(request, f"{updated} user(s) have been deactivated.")
