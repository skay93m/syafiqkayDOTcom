from django.contrib import admin
<<<<<<< HEAD
<<<<<<< HEAD
from .models import Note, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'title', 'author', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'author', 'tags')
    search_fields = ('title', 'content', 'unique_id')
    readonly_fields = ('unique_id', 'created_at', 'updated_at')
    filter_horizontal = ('tags', 'connections')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'author')
        }),
        ('Metadata', {
            'fields': ('unique_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Connections', {
            'fields': ('tags', 'connections'),
            'classes': ('collapse',)
        }),
    )
=======
# from .models import YourModel  # Replace 'YourModel' with your actual model name

# Register your models here.
# admin.site.register(YourModel)  # Register your model with the admin site
>>>>>>> 1b750c1 (Refactor notoGarden app: rename to noto_garden, remove unused files, and update settings)
=======
from .models import Note, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'title', 'author', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'author', 'tags')
    search_fields = ('title', 'content', 'unique_id')
    readonly_fields = ('unique_id', 'created_at', 'updated_at')
    filter_horizontal = ('tags', 'connections')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'author')
        }),
        ('Metadata', {
            'fields': ('unique_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Connections', {
            'fields': ('tags', 'connections'),
            'classes': ('collapse',)
        }),
    )
>>>>>>> af068c0 (Add Noto Garden dashboard, graph, guide, note detail, and note form templates)
