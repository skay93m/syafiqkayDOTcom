from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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


class VisitorTracking(models.Model):
    """Track daily visitor statistics"""
    date = models.DateField(default=timezone.now, unique=True, verbose_name='日付')
    daily_visitors = models.PositiveIntegerField(default=0, verbose_name='日間訪問者数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')

    class Meta:
        verbose_name = 'Visitor Tracking'
        verbose_name_plural = 'Visitor Tracking'
        ordering = ['-date']

    def __str__(self):
        return f"Visitors on {self.date}: {self.daily_visitors}"


class VisitorSession(models.Model):
    """Track individual visitor sessions"""
    session_key = models.CharField(max_length=40, verbose_name='セッションキー')
    ip_address = models.GenericIPAddressField(verbose_name='IPアドレス')
    user_agent = models.TextField(blank=True, verbose_name='ユーザーエージェント')
    date = models.DateField(default=timezone.now, verbose_name='日付')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')

    class Meta:
        verbose_name = 'Visitor Session'
        verbose_name_plural = 'Visitor Sessions'
        unique_together = ['session_key', 'date']
        ordering = ['-created_at']

    def __str__(self):
        return f"Session {self.session_key} on {self.date}"