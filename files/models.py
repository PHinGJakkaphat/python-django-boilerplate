"""
Files Models — FileUpload for managing uploaded files.
"""

import os
import logging
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger("files")


def upload_to_path(instance, filename):
    """Organise uploaded files by date: uploads/YYYY/MM/DD/<filename>"""
    from django.utils import timezone
    now = timezone.now()
    return os.path.join("uploads", str(now.year), str(now.month).zfill(2), str(now.day).zfill(2), filename)


class FileUpload(models.Model):
    """
    Generic file upload model.

    Stores metadata alongside the file so callers can retrieve
    original filename, MIME type, and size without inspecting the file.
    """

    file = models.FileField(
        _("file"),
        upload_to=upload_to_path,
        help_text=_("The uploaded file."),
    )
    original_filename = models.CharField(
        _("original filename"),
        max_length=255,
        help_text=_("The original name of the file as uploaded by the client."),
    )
    file_type = models.CharField(
        _("file type"),
        max_length=100,
        blank=True,
        help_text=_("MIME type of the file (e.g. image/png, application/pdf)."),
    )
    file_size = models.PositiveIntegerField(
        _("file size"),
        default=0,
        help_text=_("Size of the file in bytes."),
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_files",
        verbose_name=_("uploaded by"),
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _("file upload")
        verbose_name_plural = _("file uploads")
        ordering = ["-created_at"]

    def __str__(self):
        return self.original_filename

    def save(self, *args, **kwargs):
        """Auto-populate file_size and original_filename if not set."""
        if self.file and not self.file_size:
            self.file_size = self.file.size
        if self.file and not self.original_filename:
            self.original_filename = os.path.basename(self.file.name)
        super().save(*args, **kwargs)
        logger.info("File uploaded: %s (%d bytes)", self.original_filename, self.file_size)

    @property
    def file_size_display(self):
        """Human-readable file size."""
        size = self.file_size
        for unit in ("B", "KB", "MB", "GB"):
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
