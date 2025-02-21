from rest_framework import viewsets

from trip.models import Train
from trip.serializers import TrainSerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
