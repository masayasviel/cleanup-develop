from django.apps import AppConfig


class DefaultdbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'defaultdb'
