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
    TicketViewSet,
)

router = routers.DefaultRouter()
router.register("trains", TrainViewSet)
router.register("carriages", CarriageTypeViewSet)
router.register("crews", CrewViewSet)
router.register("stations", StationViewSet)
router.register("routes", RouteViewSet)
router.register("trips", TripViewSet)
router.register("orders", OrderViewSet)
router.register("tickets", TicketViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "trip"
