"""
Django Settings — Boilerplate
Uses python-decouple for environment variable management.
"""

import os
import logging
from pathlib import Path
from decouple import config, Csv

# ============================================================
# Base Paths
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# Security
# ============================================================
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv())

# ============================================================
# Application Definition
# ============================================================
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "debug_toolbar",
    "rest_framework",
    "drf_spectacular",
]

LOCAL_APPS = [
    "accounts",
    "common",
    "files",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ============================================================
# Middleware
# ============================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # debug toolbar (after sessions)
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# ============================================================
# Templates
# ============================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ============================================================
# Database — PostgreSQL
# ============================================================
DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": config("DB_NAME", default="django_boilerplate"),
        "USER": config("DB_USER", default="postgres"),
        "PASSWORD": config("DB_PASSWORD", default="postgres"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

# ============================================================
# Custom User Model
# ============================================================
AUTH_USER_MODEL = "accounts.User"

# ============================================================
# Password Validation
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ============================================================
# Internationalization
# ============================================================
LANGUAGE_CODE = "th"
TIME_ZONE = config("TIME_ZONE", default="Asia/Bangkok")
USE_I18N = True
USE_TZ = True

# ============================================================
# Static & Media Files
# ============================================================
STATIC_URL = config("STATIC_URL", default="/static/")
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = config("MEDIA_URL", default="/media/")
MEDIA_ROOT = BASE_DIR / "media"

# ============================================================
# Default Primary Key Field
# ============================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ============================================================
# Django REST Framework
# ============================================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "common.pagination.CustomPageNumberPagination",
    "PAGE_SIZE": 20,
}

# ============================================================
# drf-spectacular (OpenAPI / ReDoc / Swagger)
# ============================================================
SPECTACULAR_SETTINGS = {
    "TITLE": "Django Boilerplate API",
    "DESCRIPTION": "API documentation for Django Boilerplate project.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "CONTACT": {"name": "Developer", "email": "dev@example.com"},
    "LICENSE": {"name": "MIT License"},
    # ReDoc settings
    "REDOC_DIST": "SIDECAR",
    # Swagger UI settings
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
}

# ============================================================
# Django Debug Toolbar
# ============================================================
INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
    "IS_RUNNING_TESTS": False,
}

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.alerts.AlertsPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]

# ============================================================
# Admin Site Customization
# ============================================================
ADMIN_SITE_HEADER = "Django Boilerplate Admin"
ADMIN_SITE_TITLE = "Django Boilerplate"
ADMIN_INDEX_TITLE = "Site Administration"

# ============================================================
# Logging Configuration
# ============================================================
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    # ---- Formatters ----
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {module}:{lineno} — {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "[{asctime}] {levelname} — {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "colored_console": {
            "()": "logging.Formatter",
            "format": "%(asctime)s %(levelname)-8s %(name)s:%(lineno)d — %(message)s",
            "datefmt": "%H:%M:%S",
        },
    },

    # ---- Filters ----
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },

    # ---- Handlers ----
    "handlers": {
        # Console — only active when DEBUG=True
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "colored_console",
        },
        # General Django log (INFO+) — rotating 10MB, 5 backups
        "django_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "django.log",
            "maxBytes": 10 * 1024 * 1024,  # 10 MB
            "backupCount": 5,
            "formatter": "verbose",
            "encoding": "utf-8",
        },
        # Error log — only ERROR+ (always active regardless of DEBUG)
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "errors.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
            "encoding": "utf-8",
        },
        # Security log
        "security_file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "security.log",
            "maxBytes": 5 * 1024 * 1024,  # 5 MB
            "backupCount": 3,
            "formatter": "verbose",
            "encoding": "utf-8",
        },
        # Mail admins on ERROR (production only)
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
            "formatter": "verbose",
        },
    },

    # ---- Loggers ----
    "loggers": {
        # Root Django logger
        "django": {
            "handlers": ["console", "django_file", "error_file"],
            "level": "INFO",
            "propagate": False,
        },
        # HTTP request logger
        "django.request": {
            "handlers": ["console", "django_file", "error_file", "mail_admins"],
            "level": "WARNING",
            "propagate": False,
        },
        # Security logger
        "django.security": {
            "handlers": ["console", "security_file", "mail_admins"],
            "level": "WARNING",
            "propagate": False,
        },
        # Database queries (DEBUG only)
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "propagate": False,
        },
        # Accounts logger — use: logging.getLogger('accounts')
        "accounts": {
            "handlers": ["console", "django_file", "error_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        # Files logger — use: logging.getLogger('files')
        "files": {
            "handlers": ["console", "django_file", "error_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        # Common logger — use: logging.getLogger('common')
        "common": {
            "handlers": ["console", "django_file", "error_file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
