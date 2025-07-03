from django.db import models

class Rirekisho(models.Model):
    version = models.PositiveIntegerField(verbose_name='バージョン')
    personal_statement = models.TextField(verbose_name='自己PR', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')

    class Meta:
        verbose_name = 'Statement'
        ordering = ['-version']

    def __str__(self):
        return f"Rirekisho v{self.version}"