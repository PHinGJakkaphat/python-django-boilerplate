"""
Accounts Views — Placeholder
"""

import logging
from django.http import JsonResponse

logger = logging.getLogger("accounts")


def health_check(request):
    """Simple health check endpoint."""
    logger.debug("Health check requested from %s", request.META.get("REMOTE_ADDR"))
    return JsonResponse({"status": "ok", "service": "accounts"})
