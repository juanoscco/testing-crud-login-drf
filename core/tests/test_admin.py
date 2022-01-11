from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):
    """ Test Admin """
    def setUp(self) :
        """ Iniciar """
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = "juanosccomori@gmail.com",
            password = "password123ñ"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = "test@gmail.com",
            password = "pass123",
            name = "test user name complete"
        )

    def test_users_listed(self):
        """ Testear que los usuarios han sido enlistado en la pagina de usuario """
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """ Prueba que la pagina editada por el usuario funciona """
        url = reverse("admin:core_user_change", args=[self.user.id]) # /admin/core/user/1 asi se veria con el reverse.
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """ testear que la pagina de crear usuario funciona """
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)