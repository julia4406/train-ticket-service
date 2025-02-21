from django.db import models
from django.db.models import CASCADE


class Train(models.Model):
    name_number = models.CharField(max_length=50)
    pseudonym = models.CharField(max_length=50, null=True, blank=True)


class CarriageType(models.Model):
    name = models.CharField(max_length=50)


class Carriage(models.Model):
    number = models.IntegerField()
    total_seats = models.IntegerField()
    type = models.ForeignKey(
        "CarriageType", on_delete=CASCADE, related_name="carriages"
    )
