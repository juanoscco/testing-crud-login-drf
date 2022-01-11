from django.db import models
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

from core import models

def sample_user(email="test@gmail.com", password="testpass123"):
    """ Crear un ejemplo de usuario """
    return get_user_model().objects.create_user(email, password)

class ModelTest(TestCase):
    def test_create_user_with_email_successful(self):
        """ Probar la creacion de un nuevo usuario con un email correctamente """
        email = "juanosccomori@gmail.com"
        password = "Testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ Testea un email para ponerlo todo en minusculas y sea normalizado """
        email = "test@GMAIL.COM"
        user = get_user_model().objects.create_user(email,"Testpass123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ Nuevo usuario email invalido """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "Testpass123")

    # PARA EL SUPER USUARIO
    def test_create_new_superuser(self):
        """ Probar la creacion del super usuario """
        email = "juanosccomori@gmail.com"
        password = "Testpass123"
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    # PARA LAS TABLAS CREADAS PARA EL USUARIO
    def test_gender(self):
        """ Probar la creacion de un campo en la tabla correspondiente """
        gender = models.Gender.objects.create(
            user = sample_user(),
            name="Rock"
        )
        self.assertEqual(str(gender), gender.name)
    
    def test_artist(self):
        """ Probar la creacion de un campo en la tabla correspondiente """
        artist = models.Artist.objects.create(
            user = sample_user(),
            name = "Green day"
        )
        self.assertEqual(str(artist), artist.name)

    def test_song(self):
        """ Probar la creacion de un campo en la tabla correspondiente """
        song = models.Song.objects.create(
            user = sample_user(),
            name = "American idiot",
            time = "2:50"
        )
        self.assertEqual(str(song), song.name)

    # Tabla super debil
    def test_album_str(self):
        """ Probar la creacion de un campo en la tabla correspondiente """
        album = models.Album.objects.create(
            user = sample_user(),
            title= "Moon Shadows",
            description = "Test description",
        )
        self.assertEqual(str(album), album.title)

    @patch("uuid.uuid4")
    def test_album_file_name_uuid(self, mock_uuid):
        """ Probar que una imagen se halla guardado en el lugar correcto """
        uuid = "test--uuid"
        mock_uuid.return_value = uuid
        file_path = models.album_image_file_path(None, "myimage.png")

        exp_path = f"uploads/image/{uuid}.png"
        self.assertEqual(file_path, exp_path)