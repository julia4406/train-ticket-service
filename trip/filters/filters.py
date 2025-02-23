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
    train = custom_filters.TrainTripFilter()

    class Meta:
        model = Trip
        fields = [
            "route",
            "crew",
            "train",
            "departure_time",
            "arrival_time",
        ]
