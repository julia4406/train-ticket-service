from datetime import datetime

import django_filters
from django.db.models import Q

from trip.filters import custom_filters
from trip.models import Route, Trip


class RouteFilter(django_filters.FilterSet):
    city = custom_filters.CitiesRouteFilter()
    source = custom_filters.SourcesRouteFilter()
    destination = custom_filters.DestinationsRouteFilter()

    class Meta:
        model = Route
        fields = ["source", "destination"]


class TripFilter(django_filters.FilterSet):
    city = custom_filters.CitiesTripFilter()
    source = custom_filters.SourcesTripFilter()
    destination = custom_filters.DestinationsTripFilter()
    crew = custom_filters.CrewTripFilter()
    train = custom_filters.TrainTripFilter()
    date = django_filters.CharFilter(method="filter_by_dates")
    arr = django_filters.CharFilter(method="filter_by_dates_arrival")
    dep = django_filters.CharFilter(method="filter_by_dates_departure")

    def filter_by_dates(self, queryset, name, value):
        if not value:
            return queryset

        date_list = value.split(",")

        query = Q()
        for date in date_list:
            date_obj = datetime.strptime(date.strip(), "%Y-%m-%d").date()
            query |= Q(departure_time__date=date_obj) | Q(arrival_time__date=date_obj)

        return queryset.filter(query).distinct()

    def filter_by_dates_arrival(self, queryset, name, value):
        if not value:
            return queryset

        date_list = value.split(",")

        query = Q()
        for date in date_list:
            date_obj = datetime.strptime(date.strip(), "%Y-%m-%d").date()
            query |= Q(arrival_time__date=date_obj)

        return queryset.filter(query).distinct()

    def filter_by_dates_departure(self, queryset, name, value):
        if not value:
            return queryset

        date_list = value.split(",")

        query = Q()
        for date in date_list:
            date_obj = datetime.strptime(date.strip(), "%Y-%m-%d").date()
            query |= Q(departure_time__date=date_obj)

        return queryset.filter(query).distinct()

    class Meta:
        model = Trip
        fields = [
            "city",
            "source",
            "destination",
            "crew",
            "train",
            "departure_time",
            "arrival_time",
            "dep",
            "arr",
            "date",
        ]


class OrderFilter(django_filters.FilterSet): ...
