import django.contrib.auth.password_validation as password_validation
from django.contrib.auth.models import User
from django.core import exceptions
from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField

from morse_api.api.models import Message, Room, UserRoom


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

        password = attrs.get("password", None)

        if password:
            errors = dict()

            try:
                password_validation.validate_password(password=password, user=user)
            except exceptions.ValidationError as e:
                errors["password"] = list(e.messages)

            if errors:
                raise exceptions.ValidationError(errors)

        return super().validate(attrs)


class MessageSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Message
        fields = ["id", "user", "body", "datetime_sent"]
        depth = 1


class RoomSerializer(ModelSerializer):
    avatar = CharField(source="avatar.public_id", read_only=True)

    class Meta:
        model = Room
        fields = "__all__"


class UserRoomSerializer(ModelSerializer):
    user = UserSerializer()
    last_message = SerializerMethodField()
    room = RoomSerializer()

    def get_last_message(self, obj):
        return MessageSerializer(obj.room.message_set.first()).data

    class Meta:
        model = UserRoom
        fields = "__all__"
        depth = 1
