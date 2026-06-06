"""
Files Serializers
"""

from rest_framework import serializers
from .models import FileUpload


class FileUploadSerializer(serializers.ModelSerializer):
    """Serializer for uploading a file."""

    file_size_display = serializers.ReadOnlyField()

    class Meta:
        model = FileUpload
        fields = [
            "id",
            "file",
            "original_filename",
            "file_type",
            "file_size",
            "file_size_display",
            "uploaded_by",
            "created_at",
        ]
        read_only_fields = ["id", "original_filename", "file_size", "file_size_display", "uploaded_by", "created_at"]

    def create(self, validated_data):
        file_obj = validated_data.get("file")
        if file_obj:
            validated_data.setdefault("original_filename", file_obj.name)
            validated_data.setdefault("file_type", getattr(file_obj, "content_type", ""))
            validated_data.setdefault("file_size", file_obj.size)
        return super().create(validated_data)


class FileUploadListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""

    file_size_display = serializers.ReadOnlyField()

    class Meta:
        model = FileUpload
        fields = [
            "id",
            "original_filename",
            "file_type",
            "file_size_display",
            "created_at",
        ]
