"""
Accounts Views — Placeholder
"""

import logging
from django.http import JsonResponse

from common.openapi_helper import swagger_auto_schema
from accounts.docs import GET_HEALTH_CHECK

logger = logging.getLogger("accounts")


@swagger_auto_schema(**GET_HEALTH_CHECK)
def health_check(request):
    """Simple health check endpoint."""
    logger.debug("Health check requested from %s", request.META.get("REMOTE_ADDR"))
    return JsonResponse({"status": "ok", "service": "accounts"})
