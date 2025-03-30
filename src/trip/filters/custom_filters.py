import django_filters
from django.db.models import Q


def get_filtered_queryset(queryset, value, field_params):
    """
    Filters queryset based on multiple fields and lookup expressions.
    """
    if not value:
        return queryset

    values_list = value.split(",")
    query = Q()
    for item in values_list:
        for field, lookup in field_params:
            query |= Q(**{f"{field}__{lookup}": item})
    return queryset.filter(query).distinct()


class CitiesRouteFilter(django_filters.CharFilter):
    """Filters by cities (source or destination)"""

    def filter(self, queryset, value):
        return get_filtered_queryset(
            queryset,
            value,
            [
                ("source__name", "icontains"),
                ("destination__name", "icontains"),
            ],
        )


class SourcesRouteFilter(django_filters.CharFilter):
    """Filters by source city"""

    def filter(self, queryset, value):
        return get_filtered_queryset(
            queryset,
            value,
            [
                ("source__name", "icontains"),
            ],
        )


class DestinationsRouteFilter(django_filters.CharFilter):
    """Filters by destination city"""

    def filter(self, queryset, value):
        query = get_filtered_queryset(
            queryset,
            value,
            [
                ("destination__name", "icontains"),
            ],
        )
        return queryset.filter(query).distinct() if query else queryset


class CitiesTripFilter(django_filters.CharFilter):
    """Filters by cities (source or destination)"""

    def filter(self, queryset, value):
        return get_filtered_queryset(
            queryset,
            value,
            [
                ("route__source__name", "icontains"),
                ("route__destination__name", "icontains"),
            ],
        )


class SourcesTripFilter(django_filters.CharFilter):
    """Filters by source city"""

    def filter(self, queryset, value):
        return get_filtered_queryset(
            queryset,
            value,
            [
                ("route__source__name", "icontains"),
            ],
        )


class DestinationsTripFilter(django_filters.CharFilter):
    """Filters by destination city"""

    def filter(self, queryset, value):
        return get_filtered_queryset(
            queryset,
            value,
            [
                ("route__destination__name", "icontains"),
            ],
        )


class CrewTripFilter(django_filters.CharFilter):
    """Filters by crew member's first or last name"""

    def filter(self, queryset, value):
        return get_filtered_queryset(
            queryset,
            value,
            [
                ("crew__first_name", "icontains"),
                ("crew__last_name__name", "icontains"),
            ],
        )


class TrainTripFilter(django_filters.CharFilter):
    """Filters by train"""

    def filter(self, queryset, value):
        return get_filtered_queryset(
            queryset,
            value,
            [
                ("train__name_number", "icontains"),
            ],
        )
