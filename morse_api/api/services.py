import json

from django.contrib.auth.models import User
from django.db.models import F

from morse_api.api.models import Message, UserRoom
from morse_api.api.serializers import MessageSerializer


def create_message(user_room: UserRoom, body: str, user: User) -> Message:
    room = user_room.room
    UserRoom.objects.filter(room=room).update(unread_messages=F("unread_messages") + 1)

    return Message.objects.create(body=body, user=user, room=room)


def mark_unread_messages_as_read(user_room: UserRoom) -> None:
    user_room.unread_messages = 0
    user_room.save()


def message_to_string_JSON(message: Message) -> str:
    return json.dumps(MessageSerializer(message).data)
