from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

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
)


class CarriageTypeViewSet(ModelViewSet):
    queryset = CarriageType.objects.all()
    serializer_class = CarriageTypeSerializer


class TrainViewSet(ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action in ["list", "retrieve"]:
            return TrainListSerializer
        return serializer


class CrewViewSet(ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class StationViewSet(ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action in ["list", "retrieve"]:
            return RouteListSerializer
        return serializer


class TripViewSet(ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TripListSerializer
        return TripSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action in ["list", "retrieve"]:
            return OrderListSerializer
        return serializer
