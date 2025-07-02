from django.contrib import admin
from .models import Rirekisho

@admin.register(Rirekisho)
class RirekishoAdmin(admin.ModelAdmin):
    list_display = ("version", "created_at")
