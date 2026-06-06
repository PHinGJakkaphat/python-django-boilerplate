"""
Files Admin
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import FileUpload


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ("original_filename", "file_type", "file_size_display", "uploaded_by", "created_at")
    list_filter = ("file_type", "created_at")
    search_fields = ("original_filename", "uploaded_by__email")
    readonly_fields = ("original_filename", "file_type", "file_size", "uploaded_by", "created_at")
    ordering = ("-created_at",)

    @admin.display(description=_("Size"))
    def file_size_display(self, obj):
        return obj.file_size_display
