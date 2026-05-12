from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from api_tracker.models import ApiLog

class Command(BaseCommand):
    help = "Delete old logs"

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            help="Delete logs older than X days"
        )
    def handle(self,*args, **kwargs):
        days=kwargs.get("days")
        if not days:
            days=getattr(settings,"API_TRACKER",{}).get("RETENTION_DAYS",7)
        cutoff=timezone.now() - timedelta(days=days)

        deleted, _ = ApiLog.objects.filter(timeStamp__lt=cutoff).delete()

        print(f"Deleted {deleted} logs older than {days} days")