# pyright:basic, reportIncompatibleMethodOverride=false
from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from morse_api.api.models import Message
from morse_api.api.serializers import MessageSerializer, UserSerializer


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


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.all()
