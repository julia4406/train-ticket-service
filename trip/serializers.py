from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from trip.models import CarriageType, Train, Crew, Station, Route, Trip


class CarriageTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarriageType
        fields = "__all__"


class TrainSerializer(serializers.ModelSerializer):
    carriage_type = serializers.PrimaryKeyRelatedField(
        queryset=CarriageType.objects.all()
    )
    total_seats = serializers.IntegerField(read_only=True)

    class Meta:
        model = Train
        fields = [
            "id",
            "name_number",
            "carriage_type",
            "carriages_quantity",
            "total_seats",
        ]


class CrewSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "full_name")
        extra_kwargs = {
            "first_name": {"write_only": True},
            "last_name": {"write_only": True},
        }


class StationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Station
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ["source", "destination", "distance"]


class TripSerializer(serializers.ModelSerializer):
    from_station = serializers.CharField(source="route.source.name", read_only=True)
    to_station = serializers.CharField(source="route.destination.name", read_only=True)
    crew = serializers.PrimaryKeyRelatedField(
        queryset=Crew.objects.all(),
        many=True
    )

    class Meta:
        model = Trip
        fields = [
            "route",
            "from_station",
            "departure_time",
            "to_station",
            "arrival_time",
            "train",
            "crew",
        ]
