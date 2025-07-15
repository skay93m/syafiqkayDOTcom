from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Rirekisho(models.Model):
    version = models.PositiveIntegerField(verbose_name='Version')
    personal_statement = models.TextField(verbose_name='Personal Statement', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Rirekisho'
        ordering = ['-version']

    def __str__(self):
        return f"Rirekisho v{self.version}"