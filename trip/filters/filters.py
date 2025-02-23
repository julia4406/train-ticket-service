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

        # def get_queryset(self):
        #     """Retrieve trips with filters"""
        #     queryset = self.queryset
        #
        #     cities = self.request.query_params.get("city")  # множинний
        #     sources = self.request.query_params.get("from")  # множинний
        #     destinations = self.request.query_params.get("to")  # множинний
        #     trip_date = self.request.query_params.get("date")
        #     trains = self.request.query_params.get("trains")  # множинний
        #
        #     if cities:
        #         city_list = cities.split(",")
        #         query = Q()
        #         for city in city_list:
        #             query |= Q(source__name__icontains=city) | Q(
        #                 destination__name__icontains=city
        #             )
        #         queryset = queryset.filter(query).distinct()
        #
        #     if sources:
        #         source_list = sources.split(",")
        #         query = Q()
        #         for source in source_list:
        #             query |= Q(source__name__icontains=source)
        #         queryset = queryset.filter(query).distinct()
        #
        #     if destinations:
        #         destination_list = destinations.split(",")
        #         query = Q()
        #         for destination in destination_list:
        #             query |= Q(destination__name__icontains=destination)
        #         queryset = queryset.filter(query).distinct()
        #
        #     if trains:
        #         train_list = trains.split(",")
        #         query = Q()
        #         for train in train_list:
        #             query |= Q(train__name_number__icontains=train)
        #         queryset = queryset.filter(query).distinct()
        #
        #     # if cites:
        #     #     queryset = queryset.filter(title__icontains=title).distinct()
        #     #
        #     # if cites:
        #     #     genres_ids = self._params_to_ints(genres)
        #     #     queryset = queryset.filter(genres__id__in=genres_ids).distinct()
        #
        #     return queryset
        #
