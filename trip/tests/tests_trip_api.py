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
            name="St1", latitude=10.0001, longitude=11.0002
        )
        self.station2 = Station.objects.create(
            name="St2", latitude=20.0001, longitude=21.0002
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

    def test_create_order_by_user_allowed(self):
        tickets_data = [
            {"car_num": 1, "seat_num": 1, "trip": self.trip.id},
            {"car_num": 1, "seat_num": 2, "trip": self.trip.id},
        ]
        order_data = {"tickets": tickets_data}

        res = self.client.post(ORDER_URL, order_data, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        order = Order.objects.get(id=res.data["id"])
        self.assertEqual(order.tickets.count(), len(tickets_data))

    def test_create_order_with_wrong_carriage_number(self):
        order_data = {
            "tickets": [
                {"car_num": 5, "seat_num": 1, "trip": self.trip.id},
            ]
        }

        res = self.client.post(ORDER_URL, order_data, format="json")
        expected_result = "carriage number must be in range [1, 4] not 5"
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["tickets"][0]["car_num"][0], expected_result)

    def test_create_order_with_wrong_seat_number(self):
        order_data = {
            "tickets": [
                {"car_num": 4, "seat_num": 51, "trip": self.trip.id},
            ]
        }

        res = self.client.post(ORDER_URL, order_data, format="json")

        expected_result = "seat number must be in range [1, 50] not 51"
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["tickets"][0]["seat_num"][0], expected_result)

    def test_perform_order_list_only_with_orders_of_current_user(self):
        order_data = {
            "tickets": [
                {"car_num": 2, "seat_num": 10, "trip": self.trip.id},
            ]
        }
        self.client.post(ORDER_URL, order_data, format="json")

        order_data = {
            "tickets": [
                {"car_num": 2, "seat_num": 12, "trip": self.trip.id},
            ]
        }
        self.client.post(ORDER_URL, order_data, format="json")

        order_data = {
            "tickets": [
                {"car_num": 2, "seat_num": 14, "trip": self.trip.id},
            ]
        }
        self.client.post(ORDER_URL, order_data, format="json")

        res = self.client.get(ORDER_URL)

        for order in res.data:
            self.assertEqual(order["created_by"], "test@test.com")

    def test_search_train_list_by_name_number(self):
        Train.objects.create(
            name_number="002T", carriages_quantity=4, carriage_type=self.carriage
        )
        Train.objects.create(
            name_number="003T", carriages_quantity=4, carriage_type=self.carriage
        )
        # res = self.client.get(TRAIN_URL + "?search=002")
        # self.assertEqual(len(res.data), 1)
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

    def test_filter_route_by_source_and_destination_or_both(self):
        station3 = Station.objects.create(
            name="St3", latitude=30.0001, longitude=21.0002
        )
        station4 = Station.objects.create(
            name="St4", latitude=30.0011, longitude=21.0002
        )
        Route.objects.create(
            source=self.station2, destination=self.station1, distance=150
        )
        Route.objects.create(source=self.station1, destination=station3, distance=100)
        Route.objects.create(source=self.station2, destination=station4, distance=150)
        res = self.client.get(ROUTE_URL + "?source=St1")
        self.assertEqual(len(res.data), 2)
        res = self.client.get(ROUTE_URL + "?destination=St2")
        self.assertEqual(len(res.data), 1)
        res = self.client.get(ROUTE_URL + "?city=St2")
        self.assertEqual(len(res.data), 3)
        res = self.client.get(ROUTE_URL + "?city=St2,st4")
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


class AdminMovieViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_user(
            email="admin@test.com", password="admin_password", is_staff=True
        )
        self.client.force_authenticate(user=self.admin)

        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="test_password"
        )

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
            name="St1", latitude=10.0001, longitude=11.0002
        )
        self.station2 = Station.objects.create(
            name="St2", latitude=20.0001, longitude=21.0002
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

    def test_admin_can_see_orders_of_all_users(self):
        self.client.force_authenticate(user=self.user)
        order_data = {
            "tickets": [
                {"car_num": 2, "seat_num": 10, "trip": self.trip.id},
            ]
        }
        self.client.post(ORDER_URL, order_data, format="json")

        self.client.force_authenticate(user=None)
        self.client.force_authenticate(user=self.admin)

        order_data = {
            "tickets": [
                {"car_num": 2, "seat_num": 12, "trip": self.trip.id},
            ]
        }
        self.client.post(ORDER_URL, order_data, format="json")

        order_data = {
            "tickets": [
                {"car_num": 2, "seat_num": 14, "trip": self.trip.id},
            ]
        }
        self.client.post(ORDER_URL, order_data, format="json")

        res = self.client.get(ORDER_URL)

        self.assertEqual(len(res.data), 3)
