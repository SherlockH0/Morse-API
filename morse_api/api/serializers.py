import django.contrib.auth.password_validation as password_validation
from django.contrib.auth.models import User
from django.core import exceptions
from rest_framework.serializers import ModelSerializer

from morse_api.api.models import Message


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate(self, attrs):
        user = User(**attrs)

        password = attrs.get("password")

        errors = dict()

        try:
            password_validation.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)

        if errors:
            raise exceptions.ValidationError(errors)

        return super().validate(attrs)


class MessageUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "id"]


class MessageSerializer(ModelSerializer):
    user = MessageUserSerializer()

    class Meta:
        model = Message
        fields = ["id", "user", "body", "datetime_sent"]
        depth = 1
