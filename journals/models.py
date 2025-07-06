
from django.db import models


from django.contrib.auth import get_user_model

class Journal(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    content = models.TextField()
    tags = models.CharField(
        max_length=200, 
        blank=True, 
        help_text="Separate multiple tags with commas (e.g., personal, reflection, development)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='journals'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('journals:journal_detail', args=[str(self.id)])

    def get_tags(self):
        """Return list of tags"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []

    def get_tags_display(self):
        """Return tags as formatted HTML"""
        tags = self.get_tags()
        if tags:
            badges = []
            for tag in tags:
                badges.append(f'<span class="badge bg-success me-1" style="background-color: #C8E6C9 !important; color: #333 !important;">{tag}</span>')
            return ' '.join(badges)
        return ''
