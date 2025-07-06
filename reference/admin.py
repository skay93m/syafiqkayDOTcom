from django.contrib import admin
from .models import Reference


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'created_at', 'updated_at']
    list_filter = ['category', 'created_at', 'updated_at', 'author']
    search_fields = ['title', 'summary', 'content', 'category']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本情報 (Basic Information)', {
            'fields': ('title', 'category', 'author')
        }),
        ('内容 (Content)', {
            'fields': ('summary', 'content', 'url')
        }),
        ('メタデータ (Metadata)', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')
    
    class Media:
        css = {
            'all': ['css/admin-extra.css']
        }
