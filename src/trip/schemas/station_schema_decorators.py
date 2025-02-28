from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from trip.serializers import StationSerializer


def station_filter_schema():
    """
    Adds to Swagger documentation all
    query params (title, genres, actors)
    """
    return extend_schema(
        parameters=[
            OpenApiParameter(
                name="search",
                description="Filter stations by name, latitude, longitude",
                required=False,
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        name="Example 1",
                        summary="partial text",
                        description="Filters by input 'Khar' and return "
                        "'Kharkiv-Pas' station",
                        value="Khar",
                    ),
                    OpenApiExample(
                        name="Example 2",
                        summary="number (ex.1)",
                        description="Filters by input '36.23' and return all "
                        "stations which latitude or longitude "
                        "includes input",
                        value="36.23",
                    ),
                    OpenApiExample(
                        name="Example 3",
                        summary="number (ex.2)",
                        description="Filters by input '7' and return all "
                        "stations which latitude or longitude "
                        "includes input",
                        value="7",
                    ),
                ],
            )
        ]
    )
