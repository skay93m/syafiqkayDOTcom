from django.contrib import admin
from .models import Rirekisho
<<<<<<< HEAD
=======

class CustomAdminSite(admin.AdminSite):
    class Media:
        css = {
            'all': ('css/admin-extra.css',)
        }

admin.site.__class__ = CustomAdminSite
>>>>>>> fec6094 (Refactor notoGarden app: rename to noto_garden, remove unused files, and update settings)

@admin.register(Rirekisho)
class RirekishoAdmin(admin.ModelAdmin):
    list_display = ("version", "created_at")
