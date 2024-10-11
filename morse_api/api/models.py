# pyright: basic, reportIncompatibleVariableOverride=false
import uuid

from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models
from django_cryptography.fields import encrypt


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    avatar = CloudinaryField("image")

    def __str__(self) -> str:
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    body = encrypt(models.TextField())
    datetime_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"@{self.datetime_sent} {self.user} said: {self.body}"

    class Meta:
        ordering = ["-datetime_sent"]


class UserRoom(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unread_messages = models.PositiveSmallIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.user} in {self.room}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = CloudinaryField()

    def __str__(self) -> str:
        return f"{self.user}'s profile"
