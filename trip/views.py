from rest_framework import viewsets

from trip.models import Train, CarriageType
from trip.serializers import TrainSerializer, CarriageTypeSerializer


class CarriageTypeViewSet(viewsets.ModelViewSet):
    queryset = CarriageType.objects.all()
    serializer_class = CarriageTypeSerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
