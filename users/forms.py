"""
Custom User Forms for Admin
"""

from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm

from .models import User


class UserCreationForm(BaseUserCreationForm):
    """Form for creating new users in the admin panel."""

    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ("email", "username", "first_name", "last_name")


class UserChangeForm(BaseUserChangeForm):
    """Form for updating users in the admin panel."""

    class Meta(BaseUserChangeForm.Meta):
        model = User
        fields = "__all__"
