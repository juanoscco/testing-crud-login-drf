from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Artist

from album.serializers import ArtistSerializer

ARTISTS_URL = reverse("album:artist-list")


class PublicArtistsApiTests(TestCase):
    """ Probar Api artist con acceso publico """
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Probar que sea requerido el login para agregar los campos """
        res = self.client.get(ARTISTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    
class PrivateArtistsApiTests(TestCase):
    """ Probar API artists accecible privadamente """
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@email.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_artist_list(self):
        """ Probar la obtencion de la lista de artistas """
        Artist.objects.create(user=self.user, name="Jhon doe") 
        Artist.objects.create(user=self.user, name="Frank sinatra")

        res = self.client.get(ARTISTS_URL)

        artists = Artist.objects.all().order_by("-name")
        serializer = ArtistSerializer(artists, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_artists_limited_to_user(self):
        """ Probar el retorno de la lista de artistas solamente con el usuario autenticado """
        user2 = get_user_model().objects.create_user(
            "other@email.com",
            "pass1234$"
        )
        Artist.objects.create(user=user2, name="Artics monkeys")
        artist = Artist.objects.create(user=self.user, name="David guetta")

        res = self.client.get(ARTISTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], artist.name)

    def test_create_artist_successful(self):
        """ crear un nombre de artista satisfactoriamente """
        payload = {
            "name":"Green day"
        }
        self.client.post(ARTISTS_URL, payload)
        exists = Artist.objects.filter(
            user= self.user,
            name = payload["name"]
        ).exists()
        self.assertTrue(exists)

    def test_create_artist_invalid(self):
        """ crear el nombre de un artista invalido sin ningun campo """
        payload = {
            "name": ""
        }
        res = self.client.post(ARTISTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)