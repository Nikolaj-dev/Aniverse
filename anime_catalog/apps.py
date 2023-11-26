from django.apps import AppConfig


class AnimeCatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'anime_catalog'

    def ready(self):
        import anime_catalog.signals
