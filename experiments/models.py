from django.db import models
from django.urls import reverse


class Experiment(models.Model):
    STATUS_CHOICES = [
        ('conceptualizing', 'Conceptualizing'),
        ('designing', 'Designing'),
        ('testing', 'Testing'),
        ('analyzing', 'Analyzing'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    hypothesis = models.TextField()
    methodology = models.TextField()
    results = models.TextField(blank=True)
    conclusions = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='conceptualizing')
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('experiments:detail', kwargs={'slug': self.slug})
        
    def get_tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]


class ExperimentResource(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.experiment.title} - {self.title}"


class ExperimentNote(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='notes')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Note for {self.experiment.title} - {self.created_at.strftime('%Y-%m-%d')}"
