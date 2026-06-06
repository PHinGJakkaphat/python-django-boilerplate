"""
Files Views
"""

import logging
from rest_framework import generics, permissions, parsers
from drf_spectacular.utils import extend_schema

from common.openapi_helper import openapi_response, swagger_auto_schema
from common.pagination import CustomPageNumberPagination

from .models import FileUpload
from .serializers import FileUploadSerializer, FileUploadListSerializer

logger = logging.getLogger("files")

# ---- OpenAPI Schema Definitions ----

GET_FILE_LIST = {
    "operation_id": "List Files",
    "operation_description": "Returns a paginated list of uploaded files for the authenticated user.",
    "responses": {
        200: openapi_response(FileUploadListSerializer, "Success"),
    },
    "tags": ["files"],
}

POST_UPLOAD_FILE = {
    "method": "POST",
    "operation_id": "Upload File",
    "operation_description": "Upload a new file. Supports multipart/form-data.",
    "responses": {
        201: openapi_response(FileUploadSerializer, "File uploaded successfully"),
        400: "Bad request — invalid file or missing fields",
    },
    "tags": ["files"],
}


# ---- Views ----

class FileUploadListView(generics.ListCreateAPIView):
    """
    GET  /files/       — list uploaded files (paginated)
    POST /files/       — upload a new file
    """

    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return FileUploadSerializer
        return FileUploadListSerializer

    def get_queryset(self):
        return FileUpload.objects.filter(uploaded_by=self.request.user).select_related("uploaded_by")

    def perform_create(self, serializer):
        file_obj = self.request.FILES.get("file")
        serializer.save(
            uploaded_by=self.request.user,
            original_filename=file_obj.name if file_obj else "",
            file_type=getattr(file_obj, "content_type", ""),
            file_size=file_obj.size if file_obj else 0,
        )
        logger.info("User %s uploaded file: %s", self.request.user, file_obj.name if file_obj else "unknown")

    @swagger_auto_schema(**GET_FILE_LIST)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(**POST_UPLOAD_FILE)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class FileUploadDetailView(generics.RetrieveDestroyAPIView):
    """
    GET    /files/<id>/  — retrieve file detail
    DELETE /files/<id>/  — delete a file
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FileUploadSerializer

    def get_queryset(self):
        return FileUpload.objects.filter(uploaded_by=self.request.user)

    @extend_schema(
        operation_id="Get File Detail",
        description="Retrieve detail of a specific uploaded file.",
        responses={
            200: openapi_response(FileUploadSerializer, "Success"),
            404: "File not found",
        },
        tags=["files"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        operation_id="Delete File",
        description="Delete an uploaded file. Only the owner can delete their files.",
        responses={
            204: "File deleted successfully",
            404: "File not found",
        },
        tags=["files"],
    )
    def delete(self, request, *args, **kwargs):
        logger.info("User %s deleted file id=%s", request.user, kwargs.get("pk"))
        return super().delete(request, *args, **kwargs)
