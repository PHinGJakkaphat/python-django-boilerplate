"""
Custom User Model — uses email as the primary login identifier.
"""

import logging
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

logger = logging.getLogger("accounts")


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model.
    - Uses email as USERNAME_FIELD (instead of username)
    - username field kept for display purposes
    - avatar support via ImageField
    """

    email = models.EmailField(_("email address"), unique=True, db_index=True)
    username = models.CharField(_("username"), max_length=150, blank=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    avatar = models.ImageField(
        _("avatar"),
        upload_to="avatars/%Y/%m/",
        null=True,
        blank=True,
        help_text=_("Profile picture"),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_("Designates whether this user should be treated as active."),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into the admin site."),
    )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # email is required by default via USERNAME_FIELD

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name or self.email.split("@")[0]

    def get_display_name(self):
        """Return username if set, otherwise derive from email."""
        return self.username or self.get_short_name()
