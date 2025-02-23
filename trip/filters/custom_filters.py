import django_filters
from django.db.models import Q


class CitiesRouteFilter(django_filters.CharFilter):
    """Filters by cities (source or destination)"""

    def filter(self, queryset, value):
        if not value:
            return queryset

        city_list = value.split(",")
        query = Q()
        for city in city_list:
            query |= Q(source__name__icontains=city) | Q(
                destination__name__icontains=city
            )
        return queryset.filter(query).distinct()


class SourcesRouteFilter(django_filters.CharFilter):
    """Filters by source city"""

    def filter(self, queryset, value):
        if not value:
            return queryset

        source_list = value.split(",")
        query = Q()
        for source in source_list:
            query |= Q(source__name__icontains=source)
        return queryset.filter(query).distinct()


class DestinationsRouteFilter(django_filters.CharFilter):
    """Filters by destination city"""

    def filter(self, queryset, value):
        if not value:
            return queryset

        destination_list = value.split(",")
        query = Q()
        for destination in destination_list:
            query |= Q(destination__name__icontains=destination)
        return queryset.filter(query).distinct()


class CitiesTripFilter(django_filters.CharFilter):
    """Filters by cities (source or destination)"""

    def filter(self, queryset, value):
        if not value:
            return queryset

        city_list = value.split(",")
        query = Q()
        for city in city_list:
            query |= Q(route__source__name__icontains=city) | Q(
                route__destination__name__icontains=city
            )
        return queryset.filter(query).distinct()


class SourcesTripFilter(django_filters.CharFilter):
    """Filters by source city"""

    def filter(self, queryset, value):
        if not value:
            return queryset

        source_list = value.split(",")
        query = Q()
        for source in source_list:
            query |= Q(route__source__name__icontains=source)
        return queryset.filter(query).distinct()


class DestinationsTripFilter(django_filters.CharFilter):
    """Filters by destination city"""

    def filter(self, queryset, value):
        if not value:
            return queryset

        destination_list = value.split(",")
        query = Q()
        for destination in destination_list:
            query |= Q(route__destination__name__icontains=destination)
        return queryset.filter(query).distinct()


class CrewTripFilter(django_filters.CharFilter):
    """Filters by crew member's first or last name"""

    def filter(self, queryset, value):
        if not value:
            return queryset

        crew_list = value.split(",")
        query = Q()
        for crew in crew_list:
            query |= Q(crew__first_name__icontains=crew) | Q(
                crew__last_name__icontains=crew
            )
        return queryset.filter(query).distinct()


class TrainTripFilter(django_filters.CharFilter):
    """Filters by train"""

    def filter(self, queryset, value):
        if not value:
            return queryset

        train_list = value.split(",")
        query = Q()
        for train in train_list:
            query |= Q(train__name_number__icontains=train)
        return queryset.filter(query).distinct()
