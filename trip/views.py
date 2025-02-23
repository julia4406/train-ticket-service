from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from trip.filters.filters import RouteFilter, TripFilter, OrderFilter
from trip.models import Train, CarriageType, Crew, Station, Route, Trip, Order, Ticket
from trip.serializers import (
    TrainSerializer,
    CarriageTypeSerializer,
    CrewSerializer,
    StationSerializer,
    RouteSerializer,
    TripSerializer,
    TripListSerializer,
    OrderSerializer,
    TicketSerializer,
    OrderListSerializer,
    RouteListSerializer,
    TrainListSerializer,
    TripDetailSerializer,
    RouteDetailSerializer,
)


class CarriageTypeViewSet(ModelViewSet):
    queryset = CarriageType.objects.all()
    serializer_class = CarriageTypeSerializer
    filter_backends = [SearchFilter]
    search_fields = [
        "category",
        "seats_in_car",
    ]


class TrainViewSet(ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name_number"]

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action in ["list", "retrieve"]:
            return TrainListSerializer
        return serializer


class CrewViewSet(ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    filter_backends = [SearchFilter]
    search_fields = ["first_name", "last_name"]


class StationViewSet(ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name", "latitude", "longitude"]


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.all()
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


class TripViewSet(ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TripFilter

    def get_serializer_class(self):
        if self.action == "list":
            return TripListSerializer
        elif self.action == "retrieve":
            return TripDetailSerializer
        return TripSerializer


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["created_at"]

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Order.objects.all()

            user_filter = self.request.query_params.get("user")
            if user_filter:
                queryset = queryset.filter(user__email__icontains=user_filter)

        else:
            queryset = Order.objects.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action in ["list", "retrieve"]:
            return OrderListSerializer
        return serializer
