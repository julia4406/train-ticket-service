from django.db import transaction
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from trip.models import CarriageType, Train, Crew, Station, Route, Trip, Ticket, Order


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


class TrainListSerializer(TrainSerializer):
    carriage_type = serializers.SlugRelatedField(
        read_only=True, slug_field="category"
    )


class CrewSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

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
        fields = ["id", "source", "destination", "distance"]


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(read_only=True, slug_field="name")
    destination = serializers.SlugRelatedField(read_only=True, slug_field="name")


class RouteDetailSerializer(RouteSerializer):
    source = StationSerializer(read_only=True)
    destination = StationSerializer(read_only=True)


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

    def validate(self, data):
        """Validate if arrival_time bigger than departure_time"""
        departure_time = data["departure_time"]
        arrival_time = data["arrival_time"]

        if not (departure_time <= arrival_time):
            raise serializers.ValidationError(
                {
                    f"departure_time > arrival_time: Departure time cannot "
                    f"be bigger than arrival time, check input parameters! "
                    f"Your departure_time - {departure_time}, "
                    f"arrival_time {arrival_time}."
                }
            )

        return data


class TripListSerializer(TripSerializer):
    train = serializers.SlugRelatedField(read_only=True, slug_field="name_number")
    seats_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Trip
        fields = [
            "id",
            "from_station",
            "departure_time",
            "to_station",
            "arrival_time",
            "train",
            "seats_available",
        ]


class TripDetailSerializer(TripSerializer):
    crew = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    train = serializers.SlugRelatedField(read_only=True, slug_field="name_number")
    route = RouteDetailSerializer(read_only=True)
    total_seats_capacity = serializers.IntegerField(
        source="train.total_seats", read_only=True
    )
    seats_available = serializers.IntegerField(read_only=True)
    seats_booked = serializers.IntegerField(read_only=True)

    class Meta:
        model = Trip
        fields = [
            "id",
            "route",
            "departure_time",
            "arrival_time",
            "train",
            "total_seats_capacity",
            "seats_available",
            "seats_booked",
            "crew",
        ]


class TicketSerializer(serializers.ModelSerializer):
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())

    class Meta:
        model = Ticket
        fields = ["trip", "car_num", "seat_num"]

    validators = [
        UniqueTogetherValidator(
            queryset=Ticket.objects.all(),
            fields=["car_num", "seat_num", "trip"],
            message="Booking prohibited! This place already taken!",
        )
    ]

    def validate(self, data):
        car_num = data["car_num"]
        seat_num = data["seat_num"]
        train = data["trip"].train

        total_carriages = train.carriages_quantity
        total_seats = train.carriage_type.seats_in_car

        if not (1 <= car_num <= total_carriages):
            raise serializers.ValidationError(
                {
                    "car_num": f"carriage number must be in range "
                    f"[1, {total_carriages}] not {car_num}"
                }
            )

        if not (1 <= seat_num <= total_seats):
            raise serializers.ValidationError(
                {
                    "seat_num": f"seat number must be in range "
                    f"[1, {total_seats}] not {seat_num}"
                }
            )
        return data


class TicketListSerializer(TicketSerializer):
    trip = TripListSerializer(read_only=True)


class TicketDetailSerializer(TicketSerializer):
    trip = TripDetailSerializer(read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugField(source="user", read_only=True)
    tickets = TicketSerializer(many=True, allow_empty=False)

    class Meta:
        model = Order
        fields = ["id", "created_at", "created_by", "tickets"]

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets", [])
            order = Order.objects.create(**validated_data)
            for ticket in tickets_data:
                Ticket.objects.create(order=order, **ticket)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(read_only=True, many=True)


class OrderDetailSerializer(OrderSerializer):
    tickets = TicketDetailSerializer(read_only=True, many=True)
