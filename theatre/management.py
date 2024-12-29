from django.core.management.base import BaseCommand
from theatre.models import Reservation
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Delete reservations older than 30 days"

    def handle(self, *args, **kwargs):
        threshold_date = datetime.now() - timedelta(days=30)
        old_reservations = Reservation.objects.filter(created_at__lt=threshold_date)
        count = old_reservations.count()
        old_reservations.delete()
        self.stdout.write(f"Deleted {count} old reservations.")
