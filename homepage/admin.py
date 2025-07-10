from django.contrib import admin
from .models import Rirekisho, VisitorTracking, VisitorSession

class CustomAdminSite(admin.AdminSite):
    class Media:
        css = {
            'all': ('css/admin-extra.css',)
        }

admin.site.__class__ = CustomAdminSite

@admin.register(Rirekisho)
class RirekishoAdmin(admin.ModelAdmin):
    list_display = ("version", "created_at")


@admin.register(VisitorTracking)
class VisitorTrackingAdmin(admin.ModelAdmin):
    list_display = ("date", "daily_visitors", "created_at")
    list_filter = ("date",)
    ordering = ("-date",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(VisitorSession)
class VisitorSessionAdmin(admin.ModelAdmin):
    list_display = ("session_key", "ip_address", "date", "created_at")
    list_filter = ("date", "created_at")
    search_fields = ("session_key", "ip_address")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
