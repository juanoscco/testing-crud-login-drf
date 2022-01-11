from django.db import models
from django.contrib.auth.models import (
        AbstractBaseUser, 
        BaseUserManager, 
        PermissionsMixin
)
from django.db.models.deletion import CASCADE
from django.conf import settings

import os
import uuid

# Funcion para guardar imagen del usuario
def album_image_file_path(instance, filename):
    """ Genera path para imagenes """
    ext = filename.split(".")[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join("uploads/image/", filename)


# Tabla fuerte del usuario
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """ creacion del usuario """

        if not email:
            raise ValueError("Users mst have an email")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ crear super usuario """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """ Modelo personalizado de usuario que soporta hacer login con email en vez de username """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

# Tablas debiles
class Gender(models.Model):
    """ Modelo del Genero """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class Artist(models.Model):
    """ Modelo del artista """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE
    )

    def __str__(self):
        return self.name

class Song(models.Model):
    """ Modelo de la cancion """
    name = models.CharField(max_length=255)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE
    )

    def __str__(self):
        return self.name

# Tabla super debil
class Album(models.Model):
    """ Modelo del album """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to=album_image_file_path)
    description = models.TextField()
    artists = models.ManyToManyField("Artist")
    songs = models.ManyToManyField("Song")
    genders = models.ManyToManyField("Gender")

    def __str__(self):
        return self.title