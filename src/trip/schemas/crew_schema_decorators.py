from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from trip.serializers import CrewSerializer


def crew_filter_schema():
    """
    Adds to Swagger documentation all
    query params (title, genres, actors)
    """
    return extend_schema(
        parameters=[
            OpenApiParameter(
                name="search",
                description="Filter crews by first or last name",
                required=False,
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        name="Example 1",
                        summary="Full text 1",
                        description="Filters by input 'John' and return 'John Travolta'",
                        value="John",
                    ),
                    OpenApiExample(
                        name="Example 2",
                        summary="Full text 2",
                        description="Filters by input 'John Travolta' and return 'John Travolta'",
                        value="John Travolta",
                    ),
                    OpenApiExample(
                        name="Example 3",
                        summary="partial text 1",
                        description="Filters by input 'volta' and return 'John Travolta'",
                        value="volta",
                    ),
                    OpenApiExample(
                        name="Example 4",
                        summary="partial text 2",
                        description="Filters by input 'Jo volta' and return 'John Travolta'",
                        value="jo volta",
                    ),
                ],
            )
        ]
    )
