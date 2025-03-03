from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        # noqa: E731
        from . import signals  # noqa: F401  <- Suppress the warning
