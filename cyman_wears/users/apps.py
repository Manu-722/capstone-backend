from django.apps import AppConfig
  
class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cyman_wears.users'

    def ready(self):
        # import users.signals  
         from . import signals