from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models
from django_cryptography.fields import encrypt


class Room(models.Model):
    code = models.CharField(max_length=15)


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    text = encrypt(models.TextField())
    datetime_sent = models.DateTimeField(auto_now_add=True)


class UserRoom(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = CloudinaryField()
