from django.db.models.signals import post_save
from django.dispatch import receiver
from rent.models import RentBoardgame

@receiver(post_save, sender=RentBoardgame)
def check_rental_status(sender, instance, **kwargs):
    instance.update_rental_status()