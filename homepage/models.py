from django.db import models

class Rirekisho(models.Model):
    version = models.PositiveIntegerField(verbose_name='バージョン', unique=True)
    personal_statement = models.TextField(verbose_name='statement', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')
<<<<<<< HEAD
    class Meta:
        verbose_name = '履歴書'
        verbose_name_plural = '履歴書'
=======

    class Meta:
        verbose_name = 'Statement'
>>>>>>> fec6094 (Refactor notoGarden app: rename to noto_garden, remove unused files, and update settings)
        ordering = ['-version']

    def __str__(self):
        return f"Rirekisho v{self.version}"