from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


def order_filter_schema():
    """
    Adds to Swagger documentation all
    query params (title, genres, actors)
    """
    return extend_schema(
        parameters=[
            OpenApiParameter(
                name="search",
                description="Filter orders by creation date",
                required=False,
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        name="Example 1",
                        summary="search by date",
                        description="Search by input '2025-02-22' and return "
                        "order created at this date",
                        value="2025-02-22",
                    ),
                ],
            )
        ]
    )
