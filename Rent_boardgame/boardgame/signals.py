from django.db.models.signals import post_save
from django.dispatch import receiver
from boardgame.models import Boardgame
from notifications.models import Notification
from userauths.models import User

@receiver(post_save, sender=Boardgame)
def boardgame_created(sender, instance, created, **kwargs):
    if created:
        # Code to send notification when a new boardgame is created
        users = User.objects.all()  # Get all users to send notifications
        for user in users:
            Notification.objects.create(
                recipient=user,
                actor=instance.user,
                verb='added a new boardgame',
                target=instance,  # The boardgame instance that was just created
                description=f'A new boardgame {instance.title} has been added.'
            )