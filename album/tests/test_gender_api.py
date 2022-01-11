from django.contrib.auth import get_user_model
from django.db.models.lookups import GreaterThan
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Gender
from album.serializers import GenderSerializer

GENDERS_URL = reverse("album:gender-list")

class PublicGendersApiTests(TestCase):
    """ Probar Api album gender con acceso publico """
    def setUp(self):
        self.client = APIClient()
    
    def test_login_required(self):
        """ Probar que sea requerido el login para agregar los campos """
        res = self.client.get(GENDERS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateGendersApiTests(TestCase):
    """ Probar Api gender con acceso privado """
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@email.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_genders_list(self):
        """ Probar la obtencion de la lista de generos """
        Gender.objects.create(user=self.user, name="Rock")
        Gender.objects.create(user=self.user, name="Pop")

        res = self.client.get(GENDERS_URL)

        genders = Gender.objects.all().order_by("-name")
        serializer = GenderSerializer(genders, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_genders_limited_to_user(self):
        """ Probar el retorno de la lista de generos solamente cuando el usuario esta autenticado """
        user2 = get_user_model().objects.create_user(
            "other@email.com",
            "pass1234$"
        )
        Gender.objects.create(user=user2, name="Rock")
        gender = Gender.objects.create(user=self.user, name="Classic")

        res = self.client.get(GENDERS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], gender.name)
    
    def test_create_gender_successful(self):
        """ crear el nombre de un genero satisfactoriamente """
        payload = {
            "name": "Pop"
        }
        self.client.post(GENDERS_URL, payload)
        exists = Gender.objects.filter(
            user=self.user,
            name= payload["name"]
        ).exists()
        self.assertTrue(exists)
        
    def test_create_gender_invalid(self):
        """ Crear el nombre de un artista invalido sin ningun campo"""
        payload = {
            "name" : ""
        }
        res = self.client.post(GENDERS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)