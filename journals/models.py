
from django.db import models


from django.contrib.auth import get_user_model

class Journal(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='journals'
    )
    # tags = models.ManyToManyField(
    #     'tags.Tag',
    #     blank=True,
    #     related_name='journals'
    # )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('journals:journal_detail', args=[str(self.id)])
