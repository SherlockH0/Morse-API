from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from morse_api.api.models import UserRoom


def get_room_or_404(room_name: str, user: User) -> UserRoom:
    room = get_object_or_404(UserRoom, room__name=room_name, user=user)

    return room
