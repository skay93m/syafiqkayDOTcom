from django.db import models
from django.contrib.auth import get_user_model


class Reference(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    content = models.TextField()
    url = models.URLField(blank=True, null=True)
    category = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Separate multiple categories with commas (e.g., web-development, django, python)"
    )
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

    def get_categories(self):
        """Return list of categories"""
        if self.category:
            return [cat.strip() for cat in self.category.split(',')]
        return []

    def get_categories_display(self):
        """Return categories as formatted HTML"""
        categories = self.get_categories()
        if categories:
            badges = []
            for cat in categories:
                badges.append(f'<span class="badge bg-primary me-1" style="background-color: #FFB6C1 !important; color: #333 !important;">{cat}</span>')
            return ' '.join(badges)
        return ''

    class Meta:
        ordering = ['-created_at']
