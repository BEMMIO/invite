from django.apps import AppConfig


class InviteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.invite'


    def ready(self):
        import apps.invite.signals
