from django.apps import AppConfig


class RentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rent'

    def ready(self):
        # Import the signals module and register the signal only when the app is ready
        import rent.signals