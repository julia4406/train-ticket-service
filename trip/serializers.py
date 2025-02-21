from rest_framework import serializers

from trip.models import CarriageType, Train, Crew


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
