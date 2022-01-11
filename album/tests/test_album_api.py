from re import A
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Album, Song, Artist, Gender

from album.serializers import AlbumSerializer, AlbumDetailSerializer

import os
import tempfile

from PIL import Image

ALBUM_URL = reverse("album:album-list")

# Para las imagenes
def image_upload_url(recipe_id):
    """ URL de retorno para la imagen subida """
    return reverse("album:album-upload-image", args=[recipe_id])

def detail_url(recipe_id):
    """ Retorna receta detaul url """
    return reverse("album:album-detail", args=[recipe_id])

def sample_gender(user, name="Rock"):
    """ Ejemplo de creacion de generos """
    return Gender.objects.create(user=user, name=name)

def sample_artist(user, name="Green day"):
    """ Ejemplo de creacion de artista """
    return Artist.objects.create(user=user, name=name)

def sample_song(user, name="Boulevard brocken dreams", time="3:40"):
    """ Ejemplo de creacion de cancion"""
    return Song.objects.create(user=user, name=name, time=time)

def sample_album(user, **params):
    """ Ejemplo de creacion de album"""
    defaults = {
        "title": "American idiot",
        "description": "sample description"
    }
    defaults.update(params)
    return Album.objects.create(user=user, **defaults)

class PublicAlbumApiTests(TestCase):
    """ Probar Api artist con acceso publico """
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Probar que sea requerido el login para agregar los campos """
        res = self.client.get(ALBUM_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateAlbumApiTests(TestCase):
    """ Probar Api artist con acceso privado """
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@email.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_album(self):
        """ Probar obtener la lista del album """
        sample_album(user=self.user)
        sample_album(user=self.user)

        res = self.client.get(ALBUM_URL)
        
        # se usa 'id' solo para sqlite, para postgreSQL se usa '-id'
        album = Album.objects.all().order_by("-id")
        serializer = AlbumSerializer(album, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_album_limited_to_user(self):
        """ Probar la vista de album para un usuario """
        user2 = get_user_model().objects.create_user(
            "other@email.com",
            "pass1234$"
        )

        sample_album(user=user2)
        sample_album(user=self.user)

        res = self.client.get(ALBUM_URL)

        album = Album.objects.filter(user=self.user)
        serializer = AlbumSerializer(album, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_album_detail(self):
        """ Prueba ver los detalles del album """
        album  = sample_album(user=self.user)
        album.genders.add(sample_gender(user=self.user))
        album.artists.add(sample_artist(user=self.user))
        album.songs.add(sample_song(user=self.user))

        url = detail_url(album.id)
        res = self.client.get(url)

        serializer = AlbumDetailSerializer(album)
        self.assertEqual(res.data, serializer.data)
    
    def test_create_basic_album(self):
        """ probar la creacion de un album """ 
        payload = {
            "title":"Test album",
            "description":"Test description"
        }

        res = self.client.post(ALBUM_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        album = Album.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(album, key))
    
    def test_create_album_with_artists(self):
        """ Probar crear un album con los artistas """
        artist1 = sample_artist(user=self.user, name="artist1")
        artist2 = sample_artist(user=self.user, name="artist2")
        payload = {
            "title":"sample test album",
            "artists": [artist1.id, artist2.id],
            "description": "sample description" 
        }
        res = self.client.post(ALBUM_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        album = Album.objects.get(id=res.data["id"])
        artists = album.artists.all()
        self.assertEqual(artists.count(), 2)
        self.assertIn(artist1, artists)
        self.assertIn(artist2, artists)
    
    def test_create_album_with_gender(self):
        """ Probar crear un album con los generos incluidos """ 
        gender1 = sample_gender(user=self.user, name="Rock")
        gender2 = sample_gender(user=self.user, name="Pop")
        payload = {
            "title":"sample title",
            "genders":[gender1.id, gender2.id],
            "description":"sample test description"
        }
        res = self.client.post(ALBUM_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        album = Album.objects.get(id=res.data["id"])
        genders = album.genders.all()
        self.assertEqual(genders.count(), 2)
        self.assertIn(gender1, genders)
        self.assertIn(gender2, genders)

    def test_create_album_with_songs(self):
        """ Probar crear un album con las canciones incluidas """
        song1 = sample_song(user=self.user, name="sample song", time="3:40")
        song2 = sample_song(user=self.user, name="sample song1", time="3:20")
        payload = {
            "title": "sample title3",
            "songs": [song1.id, song2.id],
            "description": "sample description"
        }
        res = self.client.post(ALBUM_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        album = Album.objects.get(id=res.data["id"])
        songs = album.songs.all()
        self.assertEqual(songs.count(), 2)
        self.assertIn(song1, songs)
        self.assertIn(song2, songs)

class AlbumImageUploadTests(TestCase):
    """ Testeo de creacion de imagenes """
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@email.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)
        self.album = sample_album(user=self.user)
    
    def tearDown(self):
        """ Eliminar una imagen """
        self.album.image.delete()
    
    def test_upload_image_to_album(self):
        """ subir una imagen al album """
        url = image_upload_url(self.album.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as nft:
            img = Image.new("RGB", (10,10))
            img.save(nft, format="JPEG")
            nft.seek(0)
            res = self.client.post(url, {"image": nft}, format="multipart")

        self.album.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("image", res.data)
        self.assertTrue(os.path.exists(self.album.image.path))
    
    def test_upload_image_bad_request(self):
        """ Prueba de subir imagen sin el formato """
        url = image_upload_url(self.album.id)
        res = self.client.post(url, {
            "image":"notim"
        },
        format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_album_by_genders(self):
        """ filtrar un album por generos """
        album1 = sample_album(user=self.user, title="sample title1")
        album2 = sample_album(user=self.user, title="sample title2")

        gender1 = sample_gender(user=self.user, name="sample gender1")
        gender2 = sample_gender(user=self.user, name="sample gender2")

        album1.genders.add(gender1)
        album2.genders.add(gender2)

        album3 = sample_album(user=self.user, title="sample title3")

        res = self.client.get(
            ALBUM_URL,
            {"genders" : "{},{}".format(gender1.id, gender2.id)}
        )

        serializer1 = AlbumSerializer(album1)
        serializer2 = AlbumSerializer(album2)
        serializer3 = AlbumSerializer(album3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_album_by_artists(self):
        """ filtrar un album por artistas """
        album1 = sample_album(user=self.user, title="sample title1")
        album2 = sample_album(user=self.user, title="sample title2")

        artist1 = sample_artist(user=self.user, name="sample artist1")
        artist2 = sample_artist(user=self.user, name="sample artist2")

        album1.artists.add(artist1)
        album2.artists.add(artist2)

        album3 = sample_album(user=self.user, title="sample title3")

        res = self.client.get(
            ALBUM_URL, 
            {"artists": "{},{}".format(artist1.id, artist2.id)}
        )

        serializer1 = AlbumSerializer(album1)
        serializer2 = AlbumSerializer(album2)
        serializer3 = AlbumSerializer(album3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_album_by_songs(self):
        """ filtrar un album por canciones """
        album1 = sample_album(user=self.user, title="sample title1")
        album2 = sample_album(user=self.user, title="sample title2")

        song1 = sample_song(user=self.user, name="test song 1", time="3:20")
        song2 = sample_song(user=self.user, name="test song 2", time="3:10")

        album1.songs.add(song1)
        album2.songs.add(song2)
        
        album3 = sample_album(user=self.user, title="sample title 3")
        res = self.client.get(
            ALBUM_URL,
            {"songs": "{},{}".format(song1.id, song2.id)}
        )

        serializer1 = AlbumSerializer(album1)
        serializer2 = AlbumSerializer(album2)
        serializer3 = AlbumSerializer(album3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)