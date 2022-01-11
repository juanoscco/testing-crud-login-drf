from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto de usuarios """
    class Meta:
        model = get_user_model()
        fields = ("email", "password", "name")
        extra_kwargs = {"password": {"write_only": True, "min_length": 6}}

    def create(self, validated_data):
        """ Crear un nuevo usuario con clave encriptada y retornarlo """
        return get_user_model().objects.create_user(**validated_data)

    # Actualizar credenciales
    def update(self, instance, validated_data):
        """ Actualizar al usuario, configura el usuario correctamente y lo retorna """
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        
        return user

class AuthTokenSerializer(serializers.Serializer):
    """Serializador para la autenticacion de usuarios por medio de tokens"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """ validar y autenticar el usuario """
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            username = email,
            password = password
        )
        if not user:
            msg = _("Unable to authenticate whit provided credentials")
            raise serializers.ValidationError(msg, code="authorization")
        
        attrs["user"] = user
        return attrs