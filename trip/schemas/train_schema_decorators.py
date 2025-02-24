from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from trip.serializers import TrainSerializer


def train_filter_schema():
    """
    Adds to Swagger documentation all
    query params (title, genres, actors)
    """
    return extend_schema(
        parameters=[
            OpenApiParameter(
                name="search",
                description="Filter trains by name_number",
                required=False,
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        name="Example 1",
                        summary="Full text",
                        description="Filters by input '743K' and return this "
                        "train data",
                        value="743K",
                    ),
                    OpenApiExample(
                        name="Example 2",
                        summary="partial text 1",
                        description="Filters by input '743' and return '743K' " "train",
                        value="743",
                    ),
                    OpenApiExample(
                        name="Example 3",
                        summary="partial text 2",
                        description="Filters by input '7' and return all trains whose name contains '7'",
                        value="7",
                    ),
                ],
            )
        ]
    )
