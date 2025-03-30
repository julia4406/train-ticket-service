from django.db.models import Count, F, Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from trip.filters.filters import RouteFilter, TripFilter
from trip.models import Train, CarriageType, Crew, Station, Route, Trip, Order, Ticket
from trip.schemas.carriage_type_schema_decorators import carriage_filter_schema
from trip.schemas.crew_schema_decorators import crew_filter_schema
from trip.schemas.order_schema_decorators import order_filter_schema

from trip.schemas.station_schema_decorators import station_filter_schema
from trip.schemas.train_schema_decorators import train_filter_schema
from trip.serializers import (
    TrainSerializer,
    CarriageTypeSerializer,
    CrewSerializer,
    StationSerializer,
    RouteSerializer,
    TripSerializer,
    TripListSerializer,
    OrderSerializer,
    OrderListSerializer,
    RouteListSerializer,
    TrainListSerializer,
    TripDetailSerializer,
    RouteDetailSerializer,
    OrderDetailSerializer,
)


@extend_schema(tags=["carriages"])
class CarriageTypeViewSet(ModelViewSet):
    queryset = CarriageType.objects.all()
    serializer_class = CarriageTypeSerializer
    filter_backends = [SearchFilter]
    search_fields = [
        "category",
        "seats_in_car",
    ]

    @carriage_filter_schema()
    def list(self, request, *args, **kwargs):
        """
        Return filtered list if query parameters exists, else - full list of items
        """
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["trains"])
class TrainViewSet(ModelViewSet):
    queryset = Train.objects.select_related("carriage_type")
    serializer_class = TrainSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name_number"]

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action in ["list", "retrieve"]:
            return TrainListSerializer
        return serializer

    @train_filter_schema()
    def list(self, request, *args, **kwargs):
        """
        Return filtered list if query parameters exists, else - full list of items
        """
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["crews"])
class CrewViewSet(ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    filter_backends = [SearchFilter]
    search_fields = ["first_name", "last_name"]

    @crew_filter_schema()
    def list(self, request, *args, **kwargs):
        """
        Return filtered list if query parameters exists, else - full list of items
        """
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["stations"])
class StationViewSet(ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name", "latitude", "longitude"]

    @station_filter_schema()
    def list(self, request, *args, **kwargs):
        """
        Return filtered list if query parameters exists, else - full list of items
        """
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["routes"])
class RouteViewSet(ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RouteFilter

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action == "list":
            return RouteListSerializer
        elif self.action == "retrieve":
            return RouteDetailSerializer
        return serializer


@extend_schema(tags=["trips"])
class TripViewSet(ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TripFilter

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            queryset = (
                queryset.select_related(
                    "route__source", "route__destination", "train"
                )
                .prefetch_related("crew", "tickets")
                .annotate(
                    seats_available=F("train__total_seats") - Count("tickets"),
                )
            )
        elif self.action == "retrieve":
            queryset = (
                queryset.select_related("route", "train")
                .prefetch_related("crew", "tickets")
                .annotate(
                    seats_booked=Count("tickets"),
                    seats_available=F("train__total_seats") - Count("tickets"),
                )
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return TripListSerializer
        elif self.action == "retrieve":
            return TripDetailSerializer
        return TripSerializer


@extend_schema(tags=["orders"])
class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["created_at"]

    def get_queryset(self):
        if self.action in ["list", "retrieve"]:
            queryset = Order.objects.select_related("user").prefetch_related(
                Prefetch(
                    "tickets", queryset=Ticket.objects.select_related("trip__route")
                )
            )
        else:
            queryset = Order.objects.all()

        if not self.request.user.is_staff:
            return queryset.filter(user=self.request.user)

        user_filter = self.request.query_params.get("user")
        if user_filter:
            queryset = queryset.filter(user__email__icontains=user_filter)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action == "list":
            return OrderListSerializer
        elif self.action == "retrieve":
            return OrderDetailSerializer
        return serializer

    @order_filter_schema()
    def list(self, request, *args, **kwargs):
        """
        Return filtered list if query parameters exists, else - full list of items
        """
        return super().list(request, *args, **kwargs)
