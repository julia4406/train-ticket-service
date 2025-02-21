from django.urls import path, include
from rest_framework import routers


router = routers.DefaultRouter()
router.register("stations", GenreViewSet)
router.register("routes", ActorViewSet)
router.register("crews", CinemaHallViewSet)
router.register("trips", MovieViewSet)
router.register("trains", MovieSessionViewSet)
router.register("train_types", MovieSessionViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "trip"
