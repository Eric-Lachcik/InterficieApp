from django.apps import AppConfig


class FitcorebackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'FitCoreBack'

    def ready(self):
        import FitCoreBack.signals  