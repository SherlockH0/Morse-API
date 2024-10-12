from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from morse_api.api.views import (
    MessageListView,
    UserAvatarUploadView,
    UserRoomViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"rooms", UserRoomViewSet, basename="room")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/avatar/", UserAvatarUploadView.as_view(), name="user_avatar"),
    path("api/", include(router.urls)),
    path(
        "api/messages/<str:room_name>/", MessageListView.as_view(), name="message_list"
    ),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api-auth/", include("rest_framework.urls")),
]
