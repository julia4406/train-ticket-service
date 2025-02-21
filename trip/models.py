from django.db import models
from django.db.models import CASCADE


class Train(models.Model):
    name_number = models.CharField(max_length=50)
    carriages_quantity = models.IntegerField()
    carriage_type = models.ForeignKey(
        "CarriageType", on_delete=CASCADE, related_name="carriages"
    )
    total_seats = models.IntegerField()

    def __str__(self):
        return self.name_number


class CarriageType(models.Model):
    category = models.CharField(max_length=50)
    seats_in_car = models.IntegerField()

    def __str__(self):
        return self.category
