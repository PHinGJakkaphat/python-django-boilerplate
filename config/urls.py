"""
URL Configuration — Django Boilerplate
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# ---- Customize Admin Site ----
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Users
    path("users/", include("users.urls", namespace="users")),

    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="api-schema"), name="api-redoc"),
    path("api/docs/swagger/", SpectacularSwaggerView.as_view(url_name="api-schema"), name="api-swagger"),
]

# ---- Debug Toolbar (DEBUG mode only) ----
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns

# ---- Serve Media & Static in Development ----
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
