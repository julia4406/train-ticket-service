from django.db import models
from django.db.models import CASCADE
from django.db.models.constraints import UniqueConstraint

from train_ticket_service.settings import AUTH_USER_MODEL


class CarriageType(models.Model):
    category = models.CharField(max_length=63)
    seats_in_car = models.PositiveIntegerField()

    def __str__(self):
        return self.category


class Train(models.Model):
    name_number = models.CharField(max_length=63)
    carriages_quantity = models.PositiveIntegerField()
    carriage_type = models.ForeignKey(
        "CarriageType", on_delete=CASCADE, related_name="carriages"
    )
    total_seats = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.name_number

    def save(self, *args, **kwargs):
        self.total_seats = self.carriages_quantity * self.carriage_type.seats_in_car
        super().save(*args, **kwargs)


class Crew(models.Model):
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)

    def __str__(self):
        return self.first_name + " " + self.last_name

    @property
    def full_name(self):
        return str(self)


class Station(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey("Station", on_delete=CASCADE, related_name="sources")
    destination = models.ForeignKey(
        "Station", on_delete=CASCADE, related_name="destinations"
    )
    distance = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.source} - {self.destination} ({self.distance})"


class Trip(models.Model):
    route = models.ForeignKey("Route", on_delete=CASCADE, related_name="trips")
    crew = models.ManyToManyField("Crew", related_name="trips", blank=True)
    train = models.ForeignKey("Train", on_delete=CASCADE, related_name="trips")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return (
            f"{self.route} / departing: {self.departure_time} "
            f"/arrival: {self.arrival_time}"
        )


class Ticket(models.Model):
    car_num = models.PositiveIntegerField()
    seat_num = models.PositiveIntegerField()
    trip = models.ForeignKey("Trip", on_delete=CASCADE, related_name="tickets")
    order = models.ForeignKey("Order", on_delete=CASCADE, related_name="tickets")

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["car_num", "seat_num", "trip"],
                name="unique_car_num_seat_num_trip",
            )
        ]

    def __str__(self):
        return (
            f"from {self.trip.route.source} to {self.trip.route.destination} || "
            f"car#: {self.car_num}, seat#: {self.seat_num}"
        )


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{str(self.id)} tickets: {list(self.tickets.all())}"
