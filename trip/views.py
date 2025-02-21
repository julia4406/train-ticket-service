from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from trip.models import Train, CarriageType, Crew, Station, Route, Trip
from trip.serializers import (
    TrainSerializer,
    CarriageTypeSerializer,
    CrewSerializer,
    StationSerializer,
    RouteSerializer,
    TripSerializer,
    TripListSerializer,
)


class CarriageTypeViewSet(ModelViewSet):
    queryset = CarriageType.objects.all()
    serializer_class = CarriageTypeSerializer


class TrainViewSet(ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer


class CrewViewSet(ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class StationViewSet(ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class TripViewSet(ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    #
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TripListSerializer
        return TripSerializer
