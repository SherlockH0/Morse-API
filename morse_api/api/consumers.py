# pyright: basic, reportGeneralTypeIssues=false, reportOptionalMemberAccess=false
import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import F
from django.shortcuts import get_object_or_404

from morse_api.api.models import Message, UserRoom
from morse_api.api.serializers import MessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_chatroom(self):
        chatroom = get_object_or_404(
            UserRoom, room__name=self.room_name, user=self.scope["user"]
        )

        return chatroom

    @database_sync_to_async
    def create_message(self, body):
        UserRoom.objects.filter(room=self.chatroom.room).update(
            unread_messages=F("unread_messages") + 1
        )

        return Message.objects.create(
            body=body, user=self.scope["user"], room=self.chatroom.room
        )

    @database_sync_to_async
    def view_unread_messages(self):
        self.chatroom.unread_messages = 0
        self.chatroom.save()

    @sync_to_async
    def serialize_message(self, message):
        return json.dumps(MessageSerializer(message).data)

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.chatroom = await self.get_chatroom()

        self.room_group_name = f"chat_{self.room_name}"

        await self.view_unread_messages()

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json["body"]

        message = await self.create_message(body)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": await self.serialize_message(message),
            },
        )

    async def chat_message(self, event):
        await self.view_unread_messages()
        await self.send(text_data=event["message"])
