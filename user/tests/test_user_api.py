from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# Registro
CREATE_USER_URL = reverse("user:register")
# Login
TOKEN_URL = reverse("user:login")
# Actualizacion de datos
ME_URL = reverse("user:me")

def create_user(**params):
    """ crear usuario, con todos sus datos """
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """ le da la opcion de crear un usuario, o registrar a un usuario que entra a la pagina """
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """ Probar el registro de usuario con un payload exitoso """
        payload = {
            "email": "juanosccomori@gmail.com",
            "password": "testpass",
            "name":"Test name"
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_exist(self):
        """ Probar si puede registrar un usuario existente """
        payload = {
            "email": "juanosccomori@gmail.com",
            "password": "testpass",
            "name": "test name"
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ cuando un usuario se registra la contraseña muy corta """
        payload = {
            "email": "juanosccomori@gmail.com",
            "password": "pw",
            "name": "Test name"
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    # TOKEN_URL = LOGIN 
    def test_create_token_for_user(self):
        """ Probar que el token esta creado para el nuevo usuario """
        payload = {
            "email": "test@email.com",
            "password": "testpass1234",
            "name": "Test name"
        }

        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ probar que el token no es creado con credenciales invalidas """
        create_user(email="test@email.com", password="testpass")
        payload = { "email": "test@email.com", "password": "wrong"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """ Probamos que no se crea un token si no existe el usuario """
        payload = {
            "email": "test@email.com",
            "password": "testpass",
        }

        # No le voy a poner un create_user
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """ Probar que el email y contraseña sean requeridos """
        res = self.client.post(TOKEN_URL, {"email": "one", "password": ""})
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # URL_ME
    def test_retrive_user_unathorized(self):
        """ Prueba que la authenticacion sea requerida para los usuarios y no actualice cualquiera """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTests(TestCase):
    """ Testear el API privada del usuario """
    def setUp(self):
        self.user = create_user(
            email = "test@email.com",
            password="testpass123",
            name="name"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrive_profile_success(self):
        """ Probar la obtencion de perfil para el usuario con login """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            "name": self.user.name,
            "email": self.user.email
        })

    def test_post_me_not_allowed(self):
        """ para que el usuario no agregue nuevos usuarios, si no actualize """
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """ para que el usuario solo pueda acutalizar sus datos solo si esta autenticado"""
        payload = {
            "name" : "new name",
            "password": "newpass123"
        }

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
