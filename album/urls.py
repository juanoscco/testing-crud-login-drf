from django.urls import path, include
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter

from album import views

router = DefaultRouter()
router.register("artists", views.ArtistViewSet)
router.register("genders", views.GenderViewSet)
router.register("songs", views.SongViewSet)
router.register("albums", views.AlbumViewSet)

app_name = "album"

urlpatterns = [
    path("", include(router.urls))
]