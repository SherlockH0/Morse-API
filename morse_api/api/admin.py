from django.contrib import admin

from morse_api.api.models import Message, Room

admin.site.register((Room, Message))
