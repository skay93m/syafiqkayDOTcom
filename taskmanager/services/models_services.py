# services/models_services.py
from django.db import models

class VersionMixing(models.Model):
    """
    VersionMixing model for versioning.
    """
    version = models.IntegerField(default=0)

    def __str__(self):
        return f"Version {self.version}"
    
    class Meta:
        abstract = True