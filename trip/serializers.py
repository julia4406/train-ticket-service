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
    # full_name = serializers.StringRelatedField()

    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "full_name")
        extra_kwargs = {
            "first_name": {"write_only": True},
            "last_name": {"write_only": True},
        }


class CrewDetailSerializer(CrewSerializer):
    class Meta:
        model = Crew
        fields = "__all__"


class StationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Station
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ["id", "source", "destination", "distance"]


class TripSerializer(serializers.ModelSerializer):
    from_station = serializers.CharField(source="route.source.name", read_only=True)
    to_station = serializers.CharField(source="route.destination.name", read_only=True)
    crew = serializers.PrimaryKeyRelatedField(queryset=Crew.objects.all(), many=True)

    class Meta:
        model = Trip
        fields = [
            "id",
            "route",
            "from_station",
            "departure_time",
            "to_station",
            "arrival_time",
            "train",
            "crew",
        ]


class TripListSerializer(TripSerializer):
    crew = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    train = serializers.SlugRelatedField(read_only=True, slug_field="name_number")


class TicketSerializer(serializers.ModelSerializer): ...


class OrderSerializer(serializers.ModelSerializer): ...
