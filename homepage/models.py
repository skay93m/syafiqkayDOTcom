from django.db import models

# 履歴書 / Resume

class Rirekisho(models.Model):
    version = models.PositiveIntegerField(verbose_name='バージョン')
    personal_statement = models.TextField(verbose_name='自己PR', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    # Remove work_experience and education text fields

    class Meta:
        verbose_name = '履歴書'
        ordering = ['-version']

    def __str__(self):
        return f"Rirekisho v{self.version}"

class WorkExperience(models.Model):
    rirekisho = models.ForeignKey(Rirekisho, related_name='work_experiences', on_delete=models.CASCADE)
    role = models.CharField(max_length=128)
    company = models.CharField(max_length=128)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # Null if current
    description = models.TextField(blank=True)

class Education(models.Model):
    rirekisho = models.ForeignKey(Rirekisho, related_name='educations', on_delete=models.CASCADE)
    institution = models.CharField(max_length=128)
    degree = models.CharField(max_length=128)
    field_of_study = models.CharField(max_length=128, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
