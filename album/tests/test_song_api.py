from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Song

from album.serializers import SongSerializer

SONGS_URL = reverse("album:song-list")

class PublicSongsApiTests(TestCase):
    """ Probar Api album songs con acceso publico """
    def setUp(self):
        self.client = APIClient()
    
    def test_login_required(self):
        """ Probar que sea requerido el login para agregar los campos """
        res = self.client.get(SONGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateSongsApiTests(TestCase):
    """ Probar Api album songs con acceso privado """
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@email.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)
    
    def test_retrieve_songs_list(self):
        """ Probar la creacio de canciones para el album """
        Song.objects.create(user=self.user, name="American idiot", time="3:20")
        Song.objects.create(user=self.user, name="Holiday", time="2:50")

        res = self.client.get(SONGS_URL)
        
        songs = Song.objects.all().order_by("-name")
        serializer = SongSerializer(songs, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_songs_limited_to_user(self):
        """ Probar el retorno de la lista de canciones solamente cuando el usuario esta autenticado """
        user2 = get_user_model().objects.create_user(
            "other@email",
            "pass1234$"
        )
        Song.objects.create(user=user2, name="Jesus of suburbia", time="09:10:00")
        song = Song.objects.create(user=self.user, name="St jimmy", time="03:40:00")

        res = self.client.get(SONGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]["name"], song.name)
        self.assertEqual(res.data[0]["time"], song.time)

    def test_create_song_successful(self):
        """ Crear el nombre de una cancion satisfactoriamente """
        payload = {
            "name": "American idiot",
            "time": "02:50:00"
        }
        self.client.post(SONGS_URL, payload)
        exists = Song.objects.filter(
            user=self.user,
            name=payload["name"],
            time=payload["time"]
        ).exists()
        self.assertTrue(exists)

    def test_create_song_invalid(self):
        """ Crear el nombre de una cancion invalida sin ningun campo """
        payload = {
            "name":"",
            "time":"2:00"
        }

        res = self.client.post(SONGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)