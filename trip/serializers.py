from rest_framework import serializers

from trip import models


class CarriageTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CarriageType
        fields = "__all__"


class TrainSerializer(serializers.ModelSerializer):
    carriage_type = serializers.PrimaryKeyRelatedField(
        queryset=models.CarriageType.objects.all()
    )
    total_seats = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Train
        fields = [
            "id",
            "name_number",
            "carriage_type",
            "carriages_quantity",
            "total_seats",
        ]
