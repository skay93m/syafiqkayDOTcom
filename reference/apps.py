from django.apps import AppConfig

<<<<<<<< HEAD:reference/apps.py

class ReferenceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reference'
========
class NotoGardenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'noto_garden'
>>>>>>>> 1b750c1 (Refactor notoGarden app: rename to noto_garden, remove unused files, and update settings):noto_garden/apps.py
