from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics, authentication, permissions
from rest_framework import status
from rest_framework.response import Response

from rest_framework.settings import api_settings

class CreateUserView(generics.CreateAPIView):
    """ Crear un nuevo usuario """
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """ Crear un nuevo auth token para el usuario """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManagerUserView(generics.RetrieveUpdateAPIView):
    """ Manejar el usuario autenticado """
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """ Obtener y retornar el usuario autenticado """
        return self.request.user

class Logout(generics.GenericAPIView):
    serializer_class = AuthTokenSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
