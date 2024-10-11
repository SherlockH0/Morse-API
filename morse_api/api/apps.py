from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "morse_api.api"

    def ready(self):
        import morse_api.api.signals
