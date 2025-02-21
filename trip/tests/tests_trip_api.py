from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from trip.models import Train, CarriageType, Crew, Station
from trip.serializers import TrainSerializer, CarriageTypeSerializer, CrewSerializer

TRAIN_URL = reverse("trip:train-list")
CARRIAGE_URL = reverse("trip:carriage-list")
CREW_URL = reverse("trip:crew-list")
STATION_URL = reverse("trip:station-list")
ROUTE_URL = reverse("trip:route-list")


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

    def test_CarriageViewSet_not_allowed(self):
        res = self.client.get(CARRIAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_crews_list_display_only_full_name(self):
        crew = Crew.objects.create(first_name="Name", last_name="Surname")
        expected_data = [{"id": crew.id, "full_name": "Name Surname"}]

        res = self.client.get(CREW_URL)
        response_data = res.json()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Crew.objects.count(), 1)
        self.assertEqual(response_data, expected_data)
        self.assertNotIn("first_name", response_data[0])
        self.assertNotIn("last_name", response_data[0])

    def test_StationViewSet_not_allowed(self):
        res = self.client.get(STATION_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_route_list(self):
        res = self.client.get(ROUTE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


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

    def test_carriage_list(self):
        CarriageType.objects.create(category="test_class1", seats_in_car=50)
        CarriageType.objects.create(category="test_class2", seats_in_car=80)
        carriages = CarriageType.objects.all()

        res = self.client.get(CARRIAGE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(CarriageType.objects.count(), 2)

        serializer = CarriageTypeSerializer(carriages, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_trains_list(self):
        trains = Train.objects.all()

        res = self.client.get(TRAIN_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Train.objects.count(), 2)

        serializer = TrainSerializer(trains, many=True)
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

    def test_station_list(self):
        Station.objects.create(
            name="Test2 Station", latitude=40.4441, longitude=55.0051
        )
        Station.objects.create(
            name="Test2 Station", latitude=25.4441, longitude=40.0051
        )

        res = self.client.get(STATION_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Station.objects.count(), 2)
