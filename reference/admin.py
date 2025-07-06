from django.contrib import admin
from .models import Reference
from .forms import ReferenceForm


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    form = ReferenceForm
    list_display = ['title', 'category_display', 'author', 'created_at', 'updated_at']
    list_filter = ['category', 'created_at', 'updated_at', 'author']
    search_fields = ['title', 'summary', 'content', 'category']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本情報 (Basic Information)', {
            'fields': ('title', 'category', 'author'),
            'description': 'For multiple categories, separate with commas: web-development, django, python'
        }),
        ('内容 (Content)', {
            'fields': ('summary', 'content', 'url')
        }),
        ('メタデータ (Metadata)', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def category_display(self, obj):
        """Display categories as badges"""
        if obj.category:
            categories = [cat.strip() for cat in obj.category.split(',')]
            badges = []
            for cat in categories:
                badges.append(f'<span class="badge badge-primary" style="margin-right: 5px; background-color: #FFB6C1; color: #333;">{cat}</span>')
            return ' '.join(badges)
        return '-'
    category_display.short_description = 'Categories'
    category_display.allow_tags = True
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')
    
    class Media:
        css = {
            'all': ['css/admin-extra.css']
        }
