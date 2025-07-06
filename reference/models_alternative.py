# ALTERNATIVE APPROACH - True Many-to-Many Categories
# This would require a database migration

from django.db import models
from django.contrib.auth import get_user_model

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#FFB6C1')  # Hex color for badge
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Reference(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    content = models.TextField()
    url = models.URLField(blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True, related_name='references')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='references'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('reference:reference_detail', args=[str(self.id)])

    class Meta:
        ordering = ['-created_at']

# Admin configuration for the alternative approach
from django.contrib import admin

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_display', 'author', 'created_at']
    list_filter = ['categories', 'created_at', 'author']
    search_fields = ['title', 'summary', 'content']
    filter_horizontal = ['categories']  # Nice widget for many-to-many
    
    def category_display(self, obj):
        return ", ".join([cat.name for cat in obj.categories.all()])
    category_display.short_description = 'Categories'
