from django.contrib import admin
from .models import Rirekisho

class CustomAdminSite(admin.AdminSite):
    class Media:
        css = {
            'all': ('css/admin-extra.css',)
        }

admin.site.__class__ = CustomAdminSite

@admin.register(Rirekisho)
class RirekishoAdmin(admin.ModelAdmin):
    list_display = ("version", "created_at")
