from django.contrib import admin

from morse_api.api.models import Message, Room, UserRoom


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["__str__", "id"]


admin.site.register((Room, UserRoom))
