from django.contrib import admin
from taskmanager.models import Task, Epic, Sprint

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "status", "creator", "owner", "epic", "created_at", "updated_at")
    list_filter = ("status",)
    
    actions = ['mark_archived']
    def mark_archived(self, request, queryset):
        queryset.update(status='ARCHIVED')
    mark_archived.short_description = 'Mark selected tasks as archived'

class EpicAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "creator")
    list_filter = ("created_at",)

class SprintAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "start_date", "end_date", "creator")
    list_filter = ("end_date",)

admin.site.register(Task, TaskAdmin)
admin.site.register(Epic, EpicAdmin)
admin.site.register(Sprint, SprintAdmin)