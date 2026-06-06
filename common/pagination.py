"""
Common Pagination Classes

Usage:
    from common.pagination import CustomPageNumberPagination, LargePageNumberPagination

In settings.py:
    REST_FRAMEWORK = {
        "DEFAULT_PAGINATION_CLASS": "common.pagination.CustomPageNumberPagination",
        "PAGE_SIZE": 20,
    }
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    """
    Default pagination — 20 items per page.
    Supports ?page_size= query param (max 100).
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            "current_page": self.page.number,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        })

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "count": {
                    "type": "integer",
                    "example": 100,
                    "description": "Total number of items.",
                },
                "total_pages": {
                    "type": "integer",
                    "example": 5,
                    "description": "Total number of pages.",
                },
                "current_page": {
                    "type": "integer",
                    "example": 1,
                    "description": "Current page number.",
                },
                "next": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "example": "http://api.example.com/items/?page=2",
                },
                "previous": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "example": None,
                },
                "results": schema,
            },
        }


class LargePageNumberPagination(PageNumberPagination):
    """
    Large pagination — 100 items per page.
    Suitable for export-like endpoints or large datasets.
    Supports ?page_size= query param (max 1000).
    """

    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            "current_page": self.page.number,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        })

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "count": {
                    "type": "integer",
                    "example": 1000,
                    "description": "Total number of items.",
                },
                "total_pages": {
                    "type": "integer",
                    "example": 10,
                    "description": "Total number of pages.",
                },
                "current_page": {
                    "type": "integer",
                    "example": 1,
                    "description": "Current page number.",
                },
                "next": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "example": "http://api.example.com/items/?page=2",
                },
                "previous": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "example": None,
                },
                "results": schema,
            },
        }
