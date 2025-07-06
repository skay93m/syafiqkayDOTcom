from django.apps import AppConfig


class SyafiqkayConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'syafiqkay'
    
    def ready(self):
        # Import admin customizations after Django is ready
        from . import admin_customizations
        admin_customizations.setup_admin()
