from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from trip.models import Train, CarriageType, Crew, Station, Trip, Route
from trip.serializers import (
    TrainSerializer,
    CarriageTypeSerializer,
    CrewSerializer,
    TripSerializer,
)

TRAIN_URL = reverse("trip:train-list")
CARRIAGE_URL = reverse("trip:carriage-list")
CREW_URL = reverse("trip:crew-list")
STATION_URL = reverse("trip:station-list")
ROUTE_URL = reverse("trip:route-list")
TRIP_URL = reverse("trip:trip-list")


class UnauthenticatedUserTrainViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(CARRIAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserTrainViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="test_password"
        )
        self.client.force_authenticate(user=self.user)

        self.carriage = CarriageType.objects.create(
            category="test_class1", seats_in_car=50
        )
        self.train = Train.objects.create(
            name_number="001T", carriages_quantity=4, carriage_type=self.carriage
        )
        self.station1 = Station.objects.create(
            name="St1", latitude=10.001, longitude=11.002
        )
        self.station2 = Station.objects.create(
            name="St2", latitude=20.001, longitude=21.002
        )
        self.route = Route.objects.create(
            source=self.station1, destination=self.station2, distance=150
        )
        self.crew = Crew.objects.create(first_name="Jo", last_name="Doe")
        self.trip = Trip.objects.create(
            route=self.route,
            train=self.train,
            departure_time=make_aware(datetime(2025, 3, 24, 7, 12, 0)),
            arrival_time=make_aware(datetime(2025, 3, 24, 15, 10, 0)),
        )
        self.trip.crew.set([self.crew])

    def test_all_views_list_allowed_to_read(self):
        res = self.client.get(CARRIAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.get(TRAIN_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.get(CREW_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.get(TRIP_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.get(STATION_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.get(ROUTE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        expected_data = [{"id": self.crew.id, "full_name": "Jo Doe"}]

        res = self.client.get(CREW_URL)
        response_data = res.json()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_data, response_data)
        self.assertNotIn("first_name", response_data[0])
        self.assertNotIn("last_name", response_data[0])

    def test_trip_list_displays_correct_fields_formats(self):
        res = self.client.get(TRIP_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]["crew"], ["Jo Doe"])
        self.assertEqual(res.data[0]["train"], self.train.name_number)


class AdminMovieViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_user(
            email="admin@test.com", password="admin_password", is_staff=True
        )
        self.client.force_authenticate(user=self.admin)

        self.carriage1 = CarriageType.objects.create(
            category="test_class1", seats_in_car=50
        )
        self.carriage2 = CarriageType.objects.create(
            category="test_class2", seats_in_car=80
        )

        self.train1 = Train.objects.create(
            name_number="001T", carriages_quantity=4, carriage_type=self.carriage1
        )
        self.train2 = Train.objects.create(
            name_number="002T", carriages_quantity=2, carriage_type=self.carriage2
        )
        self.station1 = Station.objects.create(
            name="St1", latitude=10.001, longitude=11.002
        )
        self.station2 = Station.objects.create(
            name="St2", latitude=20.001, longitude=21.002
        )
        self.route = Route.objects.create(
            source=self.station1, destination=self.station2, distance=150
        )
        self.crew = Crew.objects.create(first_name="Jo", last_name="Doe")
        self.trip = Trip.objects.create(
            route=self.route,
            train=self.train1,
            departure_time=make_aware(datetime(2025, 3, 24, 7, 12, 0)),
            arrival_time=make_aware(datetime(2025, 3, 24, 15, 10, 0)),
        )
        self.trip.crew.set([self.crew])

    def test_carriage_list_create_allowed(self):
        CarriageType.objects.create(category="test_class1", seats_in_car=50)
        CarriageType.objects.create(category="test_class2", seats_in_car=80)
        carriages = CarriageType.objects.all()

        res = self.client.get(CARRIAGE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(CarriageType.objects.count(), 4)

        serializer = CarriageTypeSerializer(carriages, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_post_trains_list_with_total_seats_calculation(self):
        new = Train.objects.create(
            name_number="003T", carriages_quantity=2, carriage_type=self.carriage2
        )

        res = self.client.get(TRAIN_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Train.objects.count(), 3)

        total_seats = new.carriages_quantity * new.carriage_type.seats_in_car
        train_data = next((train for train in res.data if train["id"] == new.id), None)
        self.assertEqual(train_data["total_seats"], total_seats)
