from django.urls import path, include
from rest_framework import routers

from trip.views import TrainViewSet, CarriageTypeViewSet

router = routers.DefaultRouter()
router.register("trains", TrainViewSet)
router.register("carriages", CarriageTypeViewSet)
# router.register("stations", GenreViewSet)
# router.register("routes", ActorViewSet)
# router.register("crews", CinemaHallViewSet)
# router.register("trips", MovieViewSet)
# router.register("orders", OrderViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "trip"
