from django.apps import AppConfig


class BoardgameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'boardgame'

    def ready(self):
        # Import the signals module and register the signal only when the app is ready
        import boardgame.signals