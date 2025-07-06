from django.contrib import admin
from .models import Reference


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'created_at', 'updated_at']
    list_filter = ['category', 'created_at', 'author']
    search_fields = ['title', 'summary', 'content']
    readonly_fields = ['created_at', 'updated_at']
