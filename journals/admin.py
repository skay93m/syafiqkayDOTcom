
from django.contrib import admin
from .models import Journal


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'author']
    search_fields = ['title', 'summary', 'content']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本情報 (Basic Information)', {
            'fields': ('title', 'author')
        }),
        ('内容 (Content)', {
            'fields': ('summary', 'content')
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
