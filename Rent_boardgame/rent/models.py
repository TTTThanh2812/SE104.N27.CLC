from django.db import models
from userauths.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from notifications.signals import notify

ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('canceled', 'Canceled'),
    ]

RENTAL_STATUS_CHOICES = [
    ('active', 'Active'),
    ('replied', 'Replied'),
    ('expired', 'Expired'),
]

class RentBoardgame(models.Model):
    rid = models.AutoField(primary_key=True)
    renter = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    boardgame_numbers = models.ForeignKey('boardgame.BoardgameNumbers', 
                                          on_delete=models.CASCADE)
    rental_price = models.DecimalField(max_digits=8, decimal_places=2)
    deposit_price = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    penalty_price = models.DecimalField(max_digits=8, decimal_places=2, default='0')
    created_at = models.DateTimeField(default=timezone.now)  
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    rental_status = models.CharField(max_length=20, choices=RENTAL_STATUS_CHOICES, blank=True)
    
    class Meta:
        ordering = ['rid']

    def boardgame_rent_id(self):
        return f"{self.boardgame_numbers.boardgame.category.cid}{self.boardgame_numbers.boardgame.version.vid}{self.boardgame_numbers.boardgame.bgid}{self.boardgame_numbers.bgnid}"

    def send_expired_notification(self):
        user = self.renter
        message = "Your rental has expired."
        notify.send(self, recipient=user, verb=message)
    
    def update_rental_status(self):
        now = timezone.now().date()
        if self.rental_status == 'active':
            if now > self.end_date:
                self.rental_status = 'expired'
        elif self.rental_status == 'replied':
            self.boardgame_numbers.boardgame_number_status = 'in_stock'
        elif self.order_status == 'accepted':
            self.rental_status = 'active'

    def save(self, *args, **kwargs):
        self.update_rental_status()
        super().save(*args, **kwargs)
    

    def __str__(self):
        return f"{self.renter.username} - {self.boardgame_numbers.boardgame.title} - {self.rid}"

@receiver(post_save, sender=RentBoardgame, dispatch_uid="update_boardgame_stats_on_order_status")
def update_boardgame_stats_on_order_status(sender, instance, **kwargs):
    rental = instance
    boardgame_number = rental.boardgame_numbers

    if rental.order_status == 'pending':
        boardgame_number.boardgame.in_stock -= 1
        boardgame_number.boardgame.order += 1
    elif rental.order_status == 'canceled':
        boardgame_number.boardgame.in_stock += 1   
        boardgame_number.boardgame.order -= 1
    elif rental.order_status == 'accepted':
        boardgame_number.boardgame.order -= 1
        boardgame_number.boardgame.rental += 1
        # rental.rental_status = 'Active'

    boardgame_number.boardgame.total = boardgame_number.boardgame.in_stock + boardgame_number.boardgame.order + boardgame_number.boardgame.rental

    boardgame_number.boardgame.save()

@receiver(post_save, sender=RentBoardgame, dispatch_uid="update_boardgame_number_stats_on_order_status")
def update_boardgame_number_stats_on_order_status(sender, instance, **kwargs):
    rental = instance
    boardgame_number = rental.boardgame_numbers
    
    if rental.order_status == 'pending':
        boardgame_number.boardgame_number_status = 'order'
    elif rental.order_status == 'accepted':
        boardgame_number.boardgame_number_status ='rental'
    elif rental.order_status == 'canceled':
        boardgame_number.boardgame_number_status = 'in_stock'
        
    boardgame_number.save()
    