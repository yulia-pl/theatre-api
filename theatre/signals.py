from django.db.models.signals import post_save
from django.dispatch import receiver
from theatre.models import Reservation
from django.core.mail import send_mail


@receiver(post_save, sender=Reservation)
def send_reservation_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject="New Reservation",
            message=f"Dear {instance.user.username}, your reservation has been confirmed.",
            from_email="admin@theatre.com",
            recipient_list=[instance.user.email],
        )
