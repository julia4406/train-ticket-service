from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from trip.serializers import CarriageTypeSerializer


def carriage_filter_schema():
    """
    Adds to Swagger documentation all
    query params (title, genres, actors)
    """
    return extend_schema(
        parameters=[
            OpenApiParameter(
                name="search",
                description="Filter carriages by category or number of seats("
                "seats_in_car)",
                required=False,
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        name="Example 1",
                        summary="partial text",
                        description="Filters by input '2nd' and return '2nd class' carriages",
                        value="2nd",
                    ),
                    OpenApiExample(
                        name="Example 2",
                        summary="number (ex.1)",
                        description="Filters by input '1' and return carriages, "
                        "that includes 1 ether in 'category', or in "
                        "'seats_in_car'",
                        value="1",
                    ),
                    OpenApiExample(
                        name="Example 3",
                        summary="number (ex.2)",
                        description="Filters by input '50' and return carriages, "
                        "that includes '50' ether in 'category', or in "
                        "'seats_in_car'",
                        value="50",
                    ),
                ],
            )
        ]
    )
