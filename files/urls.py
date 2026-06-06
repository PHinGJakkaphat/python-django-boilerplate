"""
Files URL Configuration
"""

from django.urls import path
from . import views

app_name = "files"

urlpatterns = [
    path("", views.FileUploadListView.as_view(), name="file-list"),
    path("<int:pk>/", views.FileUploadDetailView.as_view(), name="file-detail"),
]
