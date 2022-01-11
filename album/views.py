from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Album, Artist, Gender, Song

from album import serializers

class BaseAlbumAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    """ Atributos base para nuestras tablas """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Retornar objetos para el usuario autenticado """
        assigned_only = bool(
            int(self.request.query_params.get("assigned_only", 0))
        )
        queryset = self.queryset

        if assigned_only:
            queryset = queryset.filter(recipe__isnull = False)
        
        return queryset.filter(
            user = self.request.user
        ).order_by("-name").distinct()

    

    def perform_create(self, serializer):
        """ Crear un nuevo campo en nuestra tabla y si no pone nada sale error """
        serializer.save(user=self.request.user)

class ArtistViewSet(BaseAlbumAttrViewSet):
    """ Manejar los campos de artista para el album"""
    queryset = Artist.objects.all()
    serializer_class = serializers.ArtistSerializer


class GenderViewSet(BaseAlbumAttrViewSet):
    """ Manejar los campos de los generos musicales para el album """
    queryset = Gender.objects.all()
    serializer_class = serializers.GenderSerializer

class SongViewSet(BaseAlbumAttrViewSet):
    """ Manejar los campos de Cancion para el album """
    queryset = Song.objects.all()
    serializer_class = serializers.SongSerializer

class AlbumViewSet(viewsets.ModelViewSet):
    """ Maneja albumes de la base de datos """
    serializer_class = serializers.AlbumSerializer
    queryset = Album.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Retornar objetos para el usuario autenticado """
        return self.queryset.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """ Retorna el detalle del album """
        if self.action == "retrieve":
            return serializers.AlbumDetailSerializer
        elif self.action == "upload_image":
            return serializers.AlbumImageSerializer
        
        return self.serializer_class
    
    def perform_create(self, serializer):
        """ Crear un nuevo campo en la tabla y no pone nada sale error """
        serializer.save(user=self.request.user)
    
    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        """ Subir imagenes al album """
        album = self.get_object()
        serializer = self.get_serializer(
            album,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def _params_to_ints(self, qs):
        """ Convertir una lista de Strings ids a lista de intergers """
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """ Obtener el album para el usuario autenticado """
        songs = self.request.query_params.get("songs")
        artists = self.request.query_params.get("artists")
        genders = self.request.query_params.get("genders")

        queryset = self.queryset
        if songs:
            songs_ids = self._params_to_ints(songs)
            queryset = queryset.filter(songs__id__in = songs_ids)
        if artists:
            artists_ids = self._params_to_ints(artists)
            queryset = queryset.filter(artists__id__in = artists_ids)
        if genders:
            genders_ids = self._params_to_ints(genders)
            queryset = queryset.filter(genders__id__in = genders_ids)
        
        return queryset.filter(user=self.request.user)