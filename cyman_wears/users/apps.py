from django.apps import AppConfig
from . import signals  
class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cyman_wears.users'

    def ready(self):
        import users.signals  