from django.core.management.base import BaseCommand
from django.utils import timezone
from homepage.models import VisitorTracking, VisitorSession
import datetime


class Command(BaseCommand):
    help = 'Clean up old visitor tracking data and maintain statistics'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=90,
            help='Number of days of data to keep (default: 90)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        days_to_keep = options['days']
        dry_run = options['dry_run']
        
        cutoff_date = timezone.now().date() - datetime.timedelta(days=days_to_keep)
        
        # Find old tracking records
        old_tracking = VisitorTracking.objects.filter(date__lt=cutoff_date)
        old_sessions = VisitorSession.objects.filter(date__lt=cutoff_date)
        
        tracking_count = old_tracking.count()
        session_count = old_sessions.count()
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'DRY RUN: Would delete {tracking_count} visitor tracking records '
                    f'and {session_count} visitor sessions older than {cutoff_date}'
                )
            )
        else:
            # Delete old records
            old_tracking.delete()
            old_sessions.delete()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully cleaned up {tracking_count} visitor tracking records '
                    f'and {session_count} visitor sessions older than {cutoff_date}'
                )
            )
        
        # Show current statistics
        total_tracking = VisitorTracking.objects.count()
        total_sessions = VisitorSession.objects.count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Current statistics: {total_tracking} tracking records, {total_sessions} sessions'
            )
        )
