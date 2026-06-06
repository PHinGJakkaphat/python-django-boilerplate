"""
common/serializers.py
─────────────────────
Provides `BaseSerializer` — a drop-in replacement for
`rest_framework.serializers.ModelSerializer` / `Serializer` that supports
an optional `examples` attribute inside `class Meta`.

How it works
────────────
When you declare `examples` in `class Meta`, `BaseSerializer` automatically
converts them into a list of `drf_spectacular.utils.OpenApiExample` objects
and stores them on the class as `_openapi_examples`.  The `swagger_auto_schema`
helper in `common.openapi_helper` reads `_openapi_examples` from any serializer
passed as `request_body` or in `responses` and injects them into the generated
schema automatically.

Usage
─────
    from common.serializers import BaseSerializer

    class UserSerializer(BaseSerializer):
        full_name = serializers.SerializerMethodField()

        def get_full_name(self, obj):
            return f"{obj.first_name} {obj.last_name}".strip()

        class Meta:
            model = User
            fields = ["id", "email", "username", "first_name", "last_name",
                      "full_name", "avatar", "date_joined"]

            # ✅ Define inline examples — they'll appear in ReDoc / Swagger UI
            examples = {
                "Basic User": {
                    "summary": "A standard user object",
                    "value": {
                        "id": 1,
                        "email": "jane@example.com",
                        "username": "jane_doe",
                        "first_name": "Jane",
                        "last_name": "Doe",
                        "full_name": "Jane Doe",
                        "avatar": "https://example.com/avatar.png",
                        "date_joined": "2024-01-15T09:30:00Z",
                    },
                },
                "Minimal User": {
                    "summary": "User with only required fields",
                    "value": {
                        "id": 2,
                        "email": "john@example.com",
                        "username": "john_doe",
                        "first_name": "",
                        "last_name": "",
                        "full_name": "",
                        "avatar": None,
                        "date_joined": "2025-03-01T00:00:00Z",
                    },
                },
            }

    # Short-form: just a flat dict (single example named "Example")
    class UserSerializer(BaseSerializer):
        class Meta:
            model = User
            fields = [...]
            examples = {
                "id": 1,
                "email": "jane@example.com",
            }
"""

from __future__ import annotations

from typing import Any

from rest_framework import serializers

try:
    from drf_spectacular.utils import OpenApiExample
    HAS_SPECTACULAR = True
except ImportError:  # pragma: no cover
    HAS_SPECTACULAR = False


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _build_openapi_examples(raw: dict) -> list:
    """
    Convert the value of ``Meta.examples`` into a list of ``OpenApiExample``.

    Supports two formats:

    1. **Multi-example dict** (recommended) — keys are example names::

        examples = {
            "Basic User": {
                "summary": "A standard user",
                "description": "Optional longer description.",
                "value": {"id": 1, "email": "jane@example.com"},
                "response_only": True,   # optional, default False
                "request_only": False,   # optional, default False
            },
        }

    2. **Flat dict** (shorthand for a single example) — if none of the
       values is itself a dict with a ``"value"`` key we treat the whole
       dict as a single example payload named ``"Example"``::

        examples = {"id": 1, "email": "jane@example.com"}
    """
    if not HAS_SPECTACULAR:
        return []

    if not isinstance(raw, dict):
        raise TypeError(
            f"Meta.examples must be a dict, got {type(raw).__name__!r}"
        )

    # Detect short-form: flat payload dict (no nested dicts with "value" keys)
    is_short_form = not any(
        isinstance(v, dict) and "value" in v for v in raw.values()
    )

    if is_short_form:
        # Treat the whole dict as a single example payload
        return [
            OpenApiExample(
                name="Example",
                value=raw,
            )
        ]

    # Multi-example form
    examples: list = []
    for name, spec in raw.items():
        if not isinstance(spec, dict):
            raise TypeError(
                f"Each entry in Meta.examples must be a dict, "
                f"got {type(spec).__name__!r} for key {name!r}"
            )

        payload = spec.get("value")
        if payload is None:
            raise ValueError(
                f"Meta.examples[{name!r}] is missing required key 'value'."
            )

        examples.append(
            OpenApiExample(
                name=name,
                summary=spec.get("summary", ""),
                description=spec.get("description", ""),
                value=payload,
                response_only=spec.get("response_only", False),
                request_only=spec.get("request_only", False),
            )
        )

    return examples


# ---------------------------------------------------------------------------
# Public base classes
# ---------------------------------------------------------------------------

class _ExamplesMixin:
    """
    Mixin that reads ``Meta.examples`` at class-creation time and stores the
    compiled ``OpenApiExample`` list on the class as ``_openapi_examples``.
    """

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

        meta = getattr(cls, "Meta", None)
        raw_examples = getattr(meta, "examples", None)

        if raw_examples is not None:
            cls._openapi_examples = _build_openapi_examples(raw_examples)
        else:
            # Inherit parent's examples if not overridden
            if not hasattr(cls, "_openapi_examples"):
                cls._openapi_examples = []


class BaseSerializer(_ExamplesMixin, serializers.Serializer):
    """
    Base class for non-model serializers.

    Supports ``Meta.examples`` for automatic ReDoc / Swagger UI example
    generation.  Use this instead of ``rest_framework.serializers.Serializer``.
    """


class BaseModelSerializer(_ExamplesMixin, serializers.ModelSerializer):
    """
    Base class for model serializers.

    Supports ``Meta.examples`` for automatic ReDoc / Swagger UI example
    generation.  Use this instead of
    ``rest_framework.serializers.ModelSerializer``.

    Example::

        class UserSerializer(BaseModelSerializer):
            class Meta:
                model = User
                fields = ["id", "email", "username"]
                examples = {
                    "Standard User": {
                        "summary": "A regular user",
                        "value": {
                            "id": 1,
                            "email": "jane@example.com",
                            "username": "jane_doe",
                        },
                    }
                }
    """
