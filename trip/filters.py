import django_filters
from django.db.models import Q

from trip.models import Route


class RouteFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(method="filter_cities")
    source = django_filters.CharFilter(method="filter_sources")
    destination = django_filters.CharFilter(method="filter_destinations")

    class Meta:
        model = Route
        fields = ["source", "destination"]

    def filter_cities(self, queryset, name, value):
        """Filters routes by cities (source or destination)"""
        if not value:
            return queryset
        city_list = value.split(",")
        query = Q()
        for city in city_list:
            query |= Q(source__name__icontains=city) | Q(
                destination__name__icontains=city
            )
        return queryset.filter(query).distinct()

    def filter_sources(self, queryset, name, value):
        """Filters routes by source city"""
        if value:
            source_list = value.split(",")
            query = Q()
            for source in source_list:
                query |= Q(source__name__icontains=source)
        return queryset.filter(query).distinct()

    def filter_destinations(self, queryset, name, value):
        """Filters routes by destination city"""
        if value:
            destination_list = value.split(",")
            query = Q()
            for destination in destination_list:
                query |= Q(destination__name__icontains=destination)
        return queryset.filter(query).distinct()
