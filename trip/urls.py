from django.urls import path, include
from rest_framework import routers

from trip.views import TrainViewSet, CarriageTypeViewSet, CrewViewSet, \
    StationViewSet, RouteViewSet

router = routers.DefaultRouter()
router.register("trains", TrainViewSet, basename="train")
router.register("carriages", CarriageTypeViewSet, basename="carriage")
router.register("crews", CrewViewSet)
router.register("stations", StationViewSet)
router.register("routes", RouteViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "trip"
