from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny

from morse_api.api.serializers import UserSerializer

# Create your views here.


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
