from rest_framework import serializers

from trip import models


class CarriageTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CarriageType
        fields = "__all__"


class TrainSerializer(serializers.ModelSerializer):
    carriages = CarriageTypeSerializer()

    class Meta:
        model = models.Train
        fields = ["id", "name_number", "carriages"]
