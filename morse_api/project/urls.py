from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from morse_api.api.views import CreateUserView, MessageListView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/messages/<str:room_name>/", MessageListView.as_view(), name="message_list"
    ),
    path("api/user/register/", CreateUserView.as_view(), name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api-auth/", include("rest_framework.urls")),
]
