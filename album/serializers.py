from rest_framework import serializers

from core.models import Album, Artist, Gender, Song

class ArtistSerializer(serializers.ModelSerializer):
    """ serializador para la tabla Artist """
    class Meta:
        model = Artist
        fields = ("id", "name")
        read_only_fields = ("id",)

class GenderSerializer(serializers.ModelSerializer):
    """ Serializador para la tabla Gender """
    class Meta:
        model = Gender
        fields = ("id", "name")
        read_only_fields = ("id",)

class SongSerializer(serializers.ModelSerializer):
    """ Serializador para la tabla Song """
    class Meta:
        model = Song
        fields = ("id", "name", "time")
        read_only_fields = ("id",)

class AlbumSerializer(serializers.ModelSerializer):
    """ Serializador para la tabla album """
    artists = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Artist.objects.all()
    )

    genders = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Gender.objects.all()
    )

    songs = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset = Song.objects.all()
    )

    class Meta:
        model = Album
        fields = (
            "id", "title","description","artists","songs","genders"
        )
        read_only_fields = ("id",)

class AlbumDetailSerializer(AlbumSerializer):
    """ Detalles del album """
    genders = GenderSerializer(many=True, read_only=True)
    songs = SongSerializer(many=True, read_only=True)
    artists = ArtistSerializer(many=True, read_only=True)

class AlbumImageSerializer(serializers.ModelSerializer):
    """ Serializador de imagenes """
    class Meta:
        model = Album
        fields = ("id", "image")
        read_only_fields = ("id",)