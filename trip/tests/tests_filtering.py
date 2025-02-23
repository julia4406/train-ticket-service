from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from trip.models import Train, CarriageType, Crew, Station, Trip, Route, Order
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
ORDER_URL = reverse("trip:order-list")


class StandardSearchFilterTests(TestCase):
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
            name="St1", latitude=10.0001, longitude=11.0002
        )
        self.station2 = Station.objects.create(
            name="St2", latitude=20.0001, longitude=21.0002
        )
        self.crew = Crew.objects.create(first_name="Jo", last_name="Doe")

    def test_search_train_list_by_name_number(self):
        Train.objects.create(
            name_number="002T", carriages_quantity=4, carriage_type=self.carriage
        )
        Train.objects.create(
            name_number="003T", carriages_quantity=4, carriage_type=self.carriage
        )
        res = self.client.get(TRAIN_URL + "?search=002")
        self.assertEqual(len(res.data), 1)
        res = self.client.get(TRAIN_URL + "?search=00")
        print(res.data)
        self.assertEqual(len(res.data), 3)
        res = self.client.get(TRAIN_URL + "?search=T")
        self.assertEqual(len(res.data), 3)

    def test_search_carriage_list_by_category_and_seats_in_car(self):
        CarriageType.objects.create(category="test_class2", seats_in_car=40)
        res = self.client.get(CARRIAGE_URL + "?search=class1")
        self.assertEqual(len(res.data), 1)
        res = self.client.get(CARRIAGE_URL + "?search=test_cla")
        self.assertEqual(len(res.data), 2)

        res = self.client.get(CARRIAGE_URL + "?search=4")
        self.assertEqual(len(res.data), 1)
        res = self.client.get(CARRIAGE_URL + "?search=0")
        self.assertEqual(len(res.data), 2)

    def test_search_crew_member_by_last_name_or_first_name(self):
        Crew.objects.create(first_name="Test", last_name="Crew")
        Crew.objects.create(first_name="Pol", last_name="Don")
        res = self.client.get(CREW_URL + "?search=do")
        self.assertEqual(len(res.data), 2)
        res = self.client.get(CREW_URL + "?search=pol")
        self.assertEqual(len(res.data), 1)
        res = self.client.get(CREW_URL + "?search=Poline")
        self.assertEqual(len(res.data), 0)

    def test_search_station_by_name_latitude_longitude(self):
        Station.objects.create(name="St2", latitude=40.4444, longitude=30.3333)
        Station.objects.create(name="St2", latitude=20.5557, longitude=25.7777)
        res = self.client.get(STATION_URL + "?search=40.4444")
        self.assertEqual(len(res.data), 1)
        res = self.client.get(STATION_URL + "?search=20")
        self.assertEqual(len(res.data), 2)

        res = self.client.get(STATION_URL + "?search=25")
        self.assertEqual(len(res.data), 1)
        res = self.client.get(STATION_URL + "?search=0")
        self.assertEqual(len(res.data), 4)


class CustomDjangoFilterBackendTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test1@test.com", password="test_password1"
        )
        self.client.force_authenticate(user=self.user)

        self.carriage = CarriageType.objects.create(
            category="test_class1", seats_in_car=50
        )
        self.train = Train.objects.create(
            name_number="001T", carriages_quantity=4, carriage_type=self.carriage
        )
        self.station1 = Station.objects.create(
            name="St1", latitude=10.0001, longitude=11.0002
        )
        self.station2 = Station.objects.create(
            name="St2", latitude=20.0001, longitude=21.0002
        )
        self.station3 = Station.objects.create(
            name="St3", latitude=30.0001, longitude=31.0002
        )
        self.station4 = Station.objects.create(
            name="St4", latitude=40.0001, longitude=41.0002
        )

        self.crew = Crew.objects.create(first_name="Joh", last_name="Doe")

        # self.trip = Trip.objects.create(
        #     route=self.route,
        #     train=self.train,
        #     departure_time=make_aware(datetime(2025, 3, 24, 7, 12, 0)),
        #     arrival_time=make_aware(datetime(2025, 3, 24, 15, 10, 0)),
        # )
        # self.trip.crew.set([self.crew])

    def test_filter_route_by_source_and_destination_or_both(self):
        Route.objects.create(
            source=self.station1, destination=self.station2, distance=150
        )
        Route.objects.create(
            source=self.station2, destination=self.station1, distance=150
        )
        Route.objects.create(
            source=self.station1, destination=self.station3, distance=150
        )
        Route.objects.create(
            source=self.station3, destination=self.station4, distance=150
        )
        res = self.client.get(ROUTE_URL + "?source=St1")
        self.assertEqual(len(res.data), 2)
        res = self.client.get(ROUTE_URL + "?destination=St2")
        self.assertEqual(len(res.data), 1)
        res = self.client.get(ROUTE_URL + "?city=St1")
        self.assertEqual(len(res.data), 3)
        res = self.client.get(ROUTE_URL + "?city=St2,st4")
        print(res.data)
        self.assertEqual(len(res.data), 3)

    # def test_search_route_by_source_and_destination(self):
    #     CarriageType.objects.create(category="test_class2", seats_in_car=40)
    #     res = self.client.get(CARRIAGE_URL + "?search=class1")
    #     self.assertEqual(len(res.data), 1)
    #     res = self.client.get(CARRIAGE_URL + "?search=test_cla")
    #     self.assertEqual(len(res.data), 2)
    #
    #     res = self.client.get(CARRIAGE_URL + "?search=4")
    #     self.assertEqual(len(res.data), 1)
    #     res = self.client.get(CARRIAGE_URL + "?search=0")
    #     self.assertEqual(len(res.data), 2)
