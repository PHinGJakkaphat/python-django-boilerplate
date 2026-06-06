"""
OpenAPI Helper — wraps drf_spectacular to provide a drf_yasg-like interface.

Designed so view-level API docs can be defined as plain dicts and applied
via the `swagger_auto_schema` decorator pattern — but powered by drf_spectacular.

Usage example:

    from common.openapi_helper import openapi_response, swagger_auto_schema
    from myapp.serializers import MyResponseSerializer

    POST_CREATE_ITEM = {
        "method": "POST",
        "operation_id": "Create Item",
        "operation_description": "Creates a new item.",
        "responses": {
            201: openapi_response(MyResponseSerializer, "Created"),
            400: "Validation error",
        },
        "tags": ["items"],
    }

    @swagger_auto_schema(**POST_CREATE_ITEM)
    def my_view(request):
        ...

Examples in serializers
───────────────────────
If a serializer inherits from `common.serializers.BaseSerializer` or
`BaseModelSerializer` and defines `examples` in its `class Meta`,
those examples are **automatically** included in the generated schema —
no extra work needed at the view level.

    class UserSerializer(BaseModelSerializer):
        class Meta:
            model = User
            fields = ["id", "email"]
            examples = {
                "Standard User": {
                    "summary": "A regular user object",
                    "value": {"id": 1, "email": "jane@example.com"},
                }
            }
"""

from typing import Union, Optional
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes


# ---------------------------------------------------------------------------
# Response helper — mirrors drf_yasg's openapi.Response(description, schema)
# ---------------------------------------------------------------------------

def openapi_response(
    serializer_or_type,
    description: str = "Success",
) -> OpenApiResponse:
    """
    Create an OpenApiResponse object for use in swagger_auto_schema `responses` dict.

    Args:
        serializer_or_type: A serializer class/instance, or a primitive OpenApiTypes value.
        description: Human-readable description of the response.

    Returns:
        OpenApiResponse compatible with drf_spectacular's @extend_schema.

    Examples:
        openapi_response(MySerializer, "Success")
        openapi_response(MySerializer(), "Created")
        openapi_response("Not found")  # description-only (no schema)
    """
    if isinstance(serializer_or_type, str):
        # Called as openapi_response("Not found") — description only, no schema
        return OpenApiResponse(description=serializer_or_type)

    # Normalise: accept both class and instance
    if isinstance(serializer_or_type, type) and issubclass(serializer_or_type, serializers.Serializer):
        schema = serializer_or_type()
    else:
        schema = serializer_or_type

    return OpenApiResponse(response=schema, description=description)


# ---------------------------------------------------------------------------
# Internal helper — collect examples from serializer _openapi_examples
# ---------------------------------------------------------------------------

def _collect_examples(serializer_or_type) -> list:
    """
    Extract ``_openapi_examples`` from a serializer class or instance.

    Returns an empty list if the serializer has no examples or if
    drf_spectacular is not installed.
    """
    if serializer_or_type is None:
        return []

    # Resolve to class
    if isinstance(serializer_or_type, serializers.Serializer):
        cls = type(serializer_or_type)
    elif isinstance(serializer_or_type, type):
        cls = serializer_or_type
    else:
        return []

    return list(getattr(cls, "_openapi_examples", []))


# ---------------------------------------------------------------------------
# Decorator helper — mirrors drf_yasg's @swagger_auto_schema(...)
# ---------------------------------------------------------------------------

def swagger_auto_schema(
    method: Optional[str] = None,
    operation_id: Optional[str] = None,
    operation_description: Optional[str] = None,
    request_body=None,
    query_serializer=None,
    responses: Optional[dict] = None,
    tags: Optional[list] = None,
    deprecated: bool = False,
    **kwargs,
):
    """
    Decorator factory that mirrors drf_yasg's @swagger_auto_schema signature
    but delegates to drf_spectacular's @extend_schema under the hood.

    Accepts a plain dict (unpacked via **) so you can define schemas as module-
    level constants and apply them with:

        @swagger_auto_schema(**MY_ENDPOINT_SCHEMA)
        def my_view(request, ...):
            ...

    Args:
        method:               HTTP method string (e.g. "GET", "POST"). Optional.
        operation_id:         Short human-readable name shown in Swagger UI.
        operation_description: Full Markdown description for the endpoint.
        request_body:         Serializer class/instance for the request body.
        query_serializer:     Serializer class/instance for query parameters.
        responses:            Dict mapping status codes → serializer / OpenApiResponse / str.
        tags:                 List of tag strings to group the endpoint in Swagger UI.
        deprecated:           Mark the endpoint as deprecated.

    Returns:
        A decorator that applies @extend_schema with translated arguments.
    """
    # Normalise responses: convert bare serializers/strings to OpenApiResponse
    normalised_responses = {}
    if responses:
        for status_code, value in responses.items():
            if isinstance(value, OpenApiResponse):
                normalised_responses[status_code] = value
            elif isinstance(value, str):
                normalised_responses[status_code] = OpenApiResponse(description=value)
            elif isinstance(value, type) and issubclass(value, serializers.Serializer):
                normalised_responses[status_code] = OpenApiResponse(response=value())
            elif isinstance(value, serializers.Serializer):
                normalised_responses[status_code] = OpenApiResponse(response=value)
            else:
                normalised_responses[status_code] = value

    # ── Auto-collect examples from serializers ──────────────────────────────
    # Gather examples defined in Meta.examples on any serializer passed as
    # request_body or as a response serializer.  Caller-supplied `examples`
    # in **kwargs always wins (merged after, so explicit ones override).
    auto_examples: list = []
    auto_examples.extend(_collect_examples(request_body))
    for value in (responses or {}).values():
        if isinstance(value, (serializers.Serializer, type)):
            auto_examples.extend(_collect_examples(value))
        elif isinstance(value, OpenApiResponse):
            # OpenApiResponse wraps a serializer in .response
            auto_examples.extend(_collect_examples(getattr(value, "response", None)))

    # Build extend_schema kwargs
    schema_kwargs = {}

    if operation_id is not None:
        schema_kwargs["operation_id"] = operation_id
    if operation_description is not None:
        schema_kwargs["description"] = operation_description
    if tags is not None:
        schema_kwargs["tags"] = tags
    if deprecated:
        schema_kwargs["deprecated"] = deprecated
    if normalised_responses:
        schema_kwargs["responses"] = normalised_responses
    if request_body is not None:
        schema_kwargs["request"] = request_body
    if query_serializer is not None:
        schema_kwargs["parameters"] = [query_serializer]

    # Merge examples: auto-collected first, then explicit caller examples
    if auto_examples:
        existing = kwargs.pop("examples", [])
        schema_kwargs["examples"] = auto_examples + list(existing)

    # Pass through any extra kwargs drf_spectacular understands
    schema_kwargs.update(kwargs)

    # Apply method filter if provided
    if method:
        schema_kwargs["methods"] = [method.upper()]

    return extend_schema(**schema_kwargs)
