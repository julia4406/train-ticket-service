from rest_framework import serializers

from trip import models


class CarriageTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CarriageType
        fields = "__all__"


class CarriageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Carriage
        fields = ["id", "number", "total_seats", "type", "train"]


class TrainSerializer(serializers.ModelSerializer):
    carriages = CarriageSerializer()

    class Meta:
        model = models.Train
        fields = ["id", "name_number", "pseudonym", "carriages"]
