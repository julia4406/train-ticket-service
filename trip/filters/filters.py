import django_filters

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

    class Meta:
        model = Trip
        fields = [
            "route__source",
            "route__destination",
            "crew__first_name",
            "crew__last_name",
            "train__name_number",
            "departure_time",
            "arrival_time",
        ]
