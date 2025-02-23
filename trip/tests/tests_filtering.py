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


class RouteFilterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test1@test.com", password="test_password1"
        )
        self.client.force_authenticate(user=self.user)

        self.carriage = CarriageType.objects.create(
            category="test_class1", seats_in_car=50
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

    def test_filter_route_by_source(self):
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
        res = self.client.get(ROUTE_URL + "?source=st1,St2")
        self.assertEqual(len(res.data), 3)
        res = self.client.get(ROUTE_URL + "?source=St4")
        self.assertEqual(len(res.data), 0)

    def test_filter_route_by_destination(self):
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

        res = self.client.get(ROUTE_URL + "?destination=St2")
        self.assertEqual(len(res.data), 1)
        res = self.client.get(ROUTE_URL + "?destination=St1,st3")
        self.assertEqual(len(res.data), 2)
        res = self.client.get(ROUTE_URL + "?destination=St2,st4,St3")
        self.assertEqual(len(res.data), 3)

    def test_filter_route_by_both_source_and_destination(self):
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

        res = self.client.get(ROUTE_URL + "?city=St2")
        self.assertEqual(len(res.data), 2)
        res = self.client.get(ROUTE_URL + "?city=St1")
        self.assertEqual(len(res.data), 3)
        res = self.client.get(ROUTE_URL + "?city=St2,st4")
        self.assertEqual(len(res.data), 3)


class TripFilterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test1@test.com", password="test_password1"
        )
        self.client.force_authenticate(user=self.user)

        self.carriage = CarriageType.objects.create(
            category="test_class1", seats_in_car=50
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

        self.route1 = Route.objects.create(
            source=self.station1, destination=self.station2, distance=150
        )
        self.route2 = Route.objects.create(
            source=self.station2, destination=self.station1, distance=150
        )
        self.route3 = Route.objects.create(
            source=self.station1, destination=self.station3, distance=150
        )
        self.route4 = Route.objects.create(
            source=self.station3, destination=self.station4, distance=150
        )
        self.train1 = Train.objects.create(
            name_number="001T", carriages_quantity=4, carriage_type=self.carriage
        )
        self.train2 = Train.objects.create(
            name_number="002T", carriages_quantity=4, carriage_type=self.carriage
        )
        self.train3 = Train.objects.create(
            name_number="003T", carriages_quantity=4, carriage_type=self.carriage
        )
        self.crew1 = Crew.objects.create(first_name="Joh", last_name="Doe")
        self.crew2 = Crew.objects.create(first_name="Red", last_name="Hat")

        self.trip1 = Trip.objects.create(
            route=self.route1,
            train=self.train1,
            departure_time=make_aware(datetime(2025, 3, 24, 7, 12, 0)),
            arrival_time=make_aware(datetime(2025, 3, 24, 15, 10, 0)),
        )
        self.trip1.crew.set([self.crew1])

        self.trip2 = Trip.objects.create(
            route=self.route2,
            train=self.train2,
            departure_time=make_aware(datetime(2025, 4, 24, 7, 12, 0)),
            arrival_time=make_aware(datetime(2025, 4, 24, 15, 10, 0)),
        )
        self.trip2.crew.set([self.crew2])

        self.trip3 = Trip.objects.create(
            route=self.route3,
            train=self.train3,
            departure_time=make_aware(datetime(2025, 4, 24, 7, 12, 0)),
            arrival_time=make_aware(datetime(2025, 4, 24, 15, 10, 0)),
        )
        self.trip3.crew.set([self.crew1, self.crew2])

        self.trip4 = Trip.objects.create(
            route=self.route4,
            train=self.train2,
            departure_time=make_aware(datetime(2025, 5, 24, 7, 12, 0)),
            arrival_time=make_aware(datetime(2025, 5, 24, 15, 10, 0)),
        )
        self.trip4.crew.set([self.crew1, self.crew2])

    def test_filter_trip_by_route_source(self):
        res = self.client.get(TRIP_URL + "?source=St1")
        self.assertEqual(len(res.data), 2)

        res = self.client.get(TRIP_URL + "?source=st1,St2")
        self.assertEqual(len(res.data), 3)

        res = self.client.get(TRIP_URL + "?source=St4")
        self.assertEqual(len(res.data), 0)

    def test_filter_route_by_destination(self):
        res = self.client.get(TRIP_URL + "?destination=St2")
        self.assertEqual(len(res.data), 1)

        res = self.client.get(TRIP_URL + "?destination=St1,st3")
        self.assertEqual(len(res.data), 2)

        res = self.client.get(TRIP_URL + "?destination=St2,st4,St3")
        self.assertEqual(len(res.data), 3)

    def test_filter_route_by_both_source_and_destination(self):
        res = self.client.get(TRIP_URL + "?city=St2")
        self.assertEqual(len(res.data), 2)

        res = self.client.get(TRIP_URL + "?city=St1")
        self.assertEqual(len(res.data), 3)

        res = self.client.get(TRIP_URL + "?city=St2,st4")
        self.assertEqual(len(res.data), 3)

    def test_filter_by_crew(self):
        res = self.client.get(TRIP_URL + "?crew=Joh")
        self.assertEqual(len(res.data), 3)

        res = self.client.get(TRIP_URL + "?crew=e")
        self.assertEqual(len(res.data), 4)

        res = self.client.get(TRIP_URL + "?crew=Hat,Red")
        self.assertEqual(len(res.data), 3)

        res = self.client.get(TRIP_URL + "?crew=Hatiko,Red")
        self.assertEqual(len(res.data), 3)

        res = self.client.get(TRIP_URL + "?crew=Hatiko")
        self.assertEqual(len(res.data), 0)
