
from django.contrib import admin
from .models import Journal
from .forms import JournalForm


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    form = JournalForm
    list_display = ['title', 'tags_display', 'author', 'created_at', 'updated_at']
    list_filter = ['tags', 'created_at', 'updated_at', 'author']
    search_fields = ['title', 'summary', 'content', 'tags']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本情報 (Basic Information)', {
            'fields': ('title', 'tags', 'author'),
            'description': 'For multiple tags, separate with commas: personal, reflection, development'
        }),
        ('内容 (Content)', {
            'fields': ('summary', 'content')
        }),
        ('メタデータ (Metadata)', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def tags_display(self, obj):
        """Display tags as badges"""
        if obj.tags:
            tags = [tag.strip() for tag in obj.tags.split(',')]
            badges = []
            for tag in tags:
                badges.append(f'<span class="badge badge-success" style="margin-right: 5px; background-color: #C8E6C9; color: #333;">{tag}</span>')
            return ' '.join(badges)
        return '-'
    tags_display.short_description = 'Tags'
    tags_display.allow_tags = True
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')
    
    class Media:
        css = {
            'all': ['css/admin-extra.css']
        }
