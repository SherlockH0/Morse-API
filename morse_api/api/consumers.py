# pyright: basic, reportGeneralTypeIssues=false, reportOptionalMemberAccess=false
import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from morse_api.api.selectors import get_room_or_404
from morse_api.api.services import (
    create_message,
    mark_unread_messages_as_read,
    message_to_string_JSON,
)


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        self.user_room = await database_sync_to_async(get_room_or_404)(
            self.room_name, self.scope["user"]
        )
        await database_sync_to_async(mark_unread_messages_as_read)(self.user_room)

        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json["body"]

        message = await database_sync_to_async(create_message)(
            self.user_room, body, self.scope["user"]
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": await sync_to_async(message_to_string_JSON)(message),
            },
        )

    async def chat_message(self, event):
        await database_sync_to_async(mark_unread_messages_as_read)(self.user_room)
        await self.send(text_data=event["message"])
