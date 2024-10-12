# pyright:basic, reportIncompatibleMethodOverride=false
import cloudinary.uploader
from cloudinary import CloudinaryImage
from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets
from rest_framework.exceptions import JsonResponse
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from morse_api.api.models import Message, UserRoom
from morse_api.api.serializers import (
    MessageSerializer,
    UserRoomSerializer,
    UserSerializer,
)


class IsUserOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow user that created an object to edit it.
    Assumes the model instance has an `user` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserOrReadOnly]


class UserAvatarUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def put(self, request, format=None):
        file_obj = request.FILES

        public_id = cloudinary.uploader.upload(file_obj["avatar"])["public_id"]

        request.user.profile.avatar = CloudinaryImage(public_id)
        request.user.profile.save()

        return JsonResponse({"avatar": public_id}, status=200)


class UserRoomViewSet(viewsets.ModelViewSet):
    serializer_class = UserRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserRoom.objects.filter(user=self.request.user)


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room = self.kwargs["room_name"]
        return Message.objects.filter(room__name=room)
