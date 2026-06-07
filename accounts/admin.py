import logging
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User
from .forms import UserCreationForm, UserChangeForm

logger = logging.getLogger("accounts")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for the custom User model."""

    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    list_display = (
        "email",
        "get_display_name",
        "get_full_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )
    list_display_links = ("email", "get_display_name")
    list_filter = ("is_active", "is_staff", "is_superuser", "date_joined")
    list_per_page = 25
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("-date_joined",)
    date_hierarchy = "date_joined"

    actions = ["activate_users", "deactivate_users"]

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

    @admin.display(description=_("Display Name"))
    def get_display_name(self, obj):
        return obj.get_display_name()

    @admin.display(description=_("Full Name"))
    def get_full_name(self, obj):
        return obj.get_full_name()

    @admin.action(description=_("Activate selected users"))
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        logger.info("Admin '%s' activated %d users.", request.user, updated)
        self.message_user(request, f"{updated} user(s) have been activated.")

    @admin.action(description=_("Deactivate selected users"))
    def deactivate_users(self, request, queryset):
        queryset = queryset.exclude(pk=request.user.pk)
        updated = queryset.update(is_active=False)
        logger.warning("Admin '%s' deactivated %d users.", request.user, updated)
        self.message_user(request, f"{updated} user(s) have been deactivated.")
