from django.urls import path, include
from rest_framework import routers

from trip.views import (
    TrainViewSet,
    CarriageTypeViewSet,
    CrewViewSet,
    StationViewSet,
    RouteViewSet,
    TripViewSet,
    OrderViewSet,
)

router = routers.DefaultRouter()
router.register("trains", TrainViewSet, basename="train")
router.register("carriages", CarriageTypeViewSet, basename="carriage")
router.register("crews", CrewViewSet, basename="crew")
router.register("stations", StationViewSet, basename="station")
router.register("routes", RouteViewSet, basename="route")
router.register("trips", TripViewSet, basename="trip")
router.register("orders", OrderViewSet, basename="order")

urlpatterns = [path("", include(router.urls))]

app_name = "trip"
