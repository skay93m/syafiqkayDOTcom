from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Experiment, ExperimentResource


class ExperimentResourceInline(admin.TabularInline):
    """Inline admin for ExperimentResource."""
    model = ExperimentResource
    extra = 1
    fields = ('title', 'url', 'description')
    show_change_link = True


@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    """Admin configuration for Experiment model."""
    
    list_display = [
        'title', 
        'status_badge', 
        'is_published', 
        'created_at', 
        'updated_at',
        'resource_count',
        'view_link'
    ]
    
    list_filter = [
        'status', 
        'is_published', 
        'created_at', 
        'updated_at'
    ]
    
    search_fields = [
        'title', 
        'description', 
        'hypothesis', 
        'methodology', 
        'tags'
    ]
    
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'tags')
        }),
        ('Experiment Details', {
            'fields': ('hypothesis', 'methodology')
        }),
        ('Results & Conclusions', {
            'fields': ('results', 'conclusions'),
            'classes': ('collapse',)
        }),
        ('Status & Publishing', {
            'fields': ('status', 'is_published')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    inlines = [ExperimentResourceInline]
    
    actions = [
        'mark_as_published', 
        'mark_as_unpublished', 
        'mark_as_completed',
        'mark_as_testing'
    ]
    
    def status_badge(self, obj):
        """Display status as a colored badge."""
        colors = {
            'conceptualizing': '#6c757d',  # gray
            'designing': '#0d6efd',        # blue
            'testing': '#fd7e14',          # orange
            'analyzing': '#6610f2',        # purple
            'completed': '#198754',        # green
            'abandoned': '#dc3545',        # red
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; '
            'border-radius: 12px; font-size: 0.8em; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def resource_count(self, obj):
        """Display count of related resources."""
        count = obj.resources.count()
        if count > 0:
            url = reverse('admin:experiments_experimentresource_changelist')
            return format_html(
                '<a href="{}?experiment__id__exact={}">{} resource{}</a>',
                url,
                obj.id,
                count,
                's' if count != 1 else ''
            )
        return '0 resources'
    resource_count.short_description = 'Resources'
    
    def view_link(self, obj):
        """Link to view experiment on frontend."""
        if obj.is_published:
            return format_html(
                '<a href="{}" target="_blank" title="View on site">👁️ View</a>',
                obj.get_absolute_url()
            )
        return mark_safe('<span style="color: #999;">Not published</span>')
    view_link.short_description = 'Frontend'
    
    def mark_as_published(self, request, queryset):
        """Mark selected experiments as published."""
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} experiment(s) marked as published.')
    mark_as_published.short_description = "Mark selected experiments as published"
    
    def mark_as_unpublished(self, request, queryset):
        """Mark selected experiments as unpublished."""
        updated = queryset.update(is_published=False)
        self.message_user(request, f'{updated} experiment(s) marked as unpublished.')
    mark_as_unpublished.short_description = "Mark selected experiments as unpublished"
    
    def mark_as_completed(self, request, queryset):
        """Mark selected experiments as completed."""
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} experiment(s) marked as completed.')
    mark_as_completed.short_description = "Mark selected experiments as completed"
    
    def mark_as_testing(self, request, queryset):
        """Mark selected experiments as testing."""
        updated = queryset.update(status='testing')
        self.message_user(request, f'{updated} experiment(s) marked as testing.')
    mark_as_testing.short_description = "Mark selected experiments as testing"


@admin.register(ExperimentResource)
class ExperimentResourceAdmin(admin.ModelAdmin):
    """Admin configuration for ExperimentResource model."""
    
    list_display = [
        'title', 
        'experiment_link', 
        'url_link', 
        'created_at'
    ]
    
    list_filter = [
        'experiment', 
        'created_at'
    ]
    
    search_fields = [
        'title', 
        'description', 
        'experiment__title'
    ]
    
    fieldsets = (
        ('Resource Information', {
            'fields': ('experiment', 'title', 'url', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at',)
    
    def experiment_link(self, obj):
        """Link to the related experiment."""
        url = reverse('admin:experiments_experiment_change', args=[obj.experiment.id])
        return format_html('<a href="{}">{}</a>', url, obj.experiment.title)
    experiment_link.short_description = 'Experiment'
    
    def url_link(self, obj):
        """Display URL as clickable link."""
        if obj.url:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.url, obj.url[:50] + '...' if len(obj.url) > 50 else obj.url)
        return '-'
    url_link.short_description = 'URL'
