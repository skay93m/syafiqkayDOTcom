from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import re

class Tag(models.Model):
    """Tags for categorizing notes"""
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default="#6c757d")  # Hex color
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Note(models.Model):
    """Zettelkasten note model"""
    
    # Core fields
    title = models.CharField(max_length=200)
    content = models.TextField()
    unique_id = models.CharField(max_length=20, unique=True, editable=False)
    
    # Metadata
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='notes'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='notes')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Zettelkasten specific
    connections = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='connected_notes'
    )
    
    def __str__(self):
        return f"{self.unique_id}: {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.unique_id:
            # Generate unique ID based on timestamp
            import datetime
            now = datetime.datetime.now()
            self.unique_id = now.strftime("%Y%m%d%H%M%S")
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('noto_garden:note_detail', args=[str(self.unique_id)])
    
    def get_backlinks(self):
        """Get notes that link to this note"""
        return Note.objects.filter(connections=self)
    
    def extract_note_links(self):
        """Extract [[note_id]] links from content"""
        pattern = r'\[\[([^\]]+)\]\]'
        return re.findall(pattern, self.content)
    
    def process_content_links(self):
        """Process content and create connections based on [[note_id]] syntax"""
        note_ids = self.extract_note_links()
        for note_id in note_ids:
            try:
                linked_note = Note.objects.get(unique_id=note_id)
                self.connections.add(linked_note)
            except Note.DoesNotExist:
                pass  # Link to non-existent note
    
    def get_connected_notes(self):
        """Get all notes connected to this note"""
        return self.connections.all()
    
    def get_word_count(self):
        """Get approximate word count of content"""
        return len(self.content.split())
    
    class Meta:
        ordering = ['-updated_at']
