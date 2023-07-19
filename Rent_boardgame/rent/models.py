from django.db import models
from userauths.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from notifications.signals import notify

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    boardgame = models.ForeignKey('boardgame.Boardgame', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    rental_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_rental_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.rental_price = self.boardgame.rental_price()
        self.total_rental_price = self.rental_price * self.quantity
        super(Cart, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.boardgame.title}"

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
    boardgame_numbers = models.ForeignKey('boardgame.BoardgameNumbers', on_delete=models.CASCADE)
    rental_price = models.DecimalField(max_digits=8, decimal_places=2)
    deposit_price = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    penalty_price = models.DecimalField(max_digits=8, decimal_places=2, default='0')
    created_at = models.DateTimeField(default=timezone.now)  
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    rental_status = models.CharField(max_length=20, choices=RENTAL_STATUS_CHOICES, blank=True, null=True)
    
    class Meta:
        ordering = ['rid']

    def boardgame_rent_id(self):
        return f"{self.boardgame_numbers.boardgame.category.cid}{self.boardgame_numbers.boardgame.version.vid}{self.boardgame_numbers.boardgame.bgid}{self.boardgame_numbers.bgnid}"

    # def send_expired_notification(self):
    #     user = self.renter
    #     message = "Your rental has expired."
    #     notify.send(self, recipient=user, verb=message)
    
    def update_rental_status(self):
        now = timezone.now().date()
        if self.rental_status == 'active':
            if now > self.end_date:
                self.rental_status = 'expired'
        elif self.order_status == 'accepted':
            if self.boardgame_numbers.boardgame_number_status == 'order':
                self.rental_status = 'active'

    def save(self, *args, **kwargs):
        self.update_rental_status()
        super().save(*args, **kwargs)
    
    def is_expired(self):
        now = timezone.now().date()
        return self.rental_status == 'active' and self.end_date < now  
    
    def get_rental_duration(self):
        duration = (self.end_date - self.start_date).days
        return duration

    def __str__(self):
        return f"{self.renter.username} - {self.boardgame_numbers.boardgame.title} - {self.rid}"

@receiver(post_save, sender=RentBoardgame, dispatch_uid="update_order_status")
def update_order_status(sender, instance, **kwargs):
    rental = instance
    boardgame_number = rental.boardgame_numbers

    if rental.order_status == 'pending':
        boardgame_number.boardgame.in_stock -= 1
        boardgame_number.boardgame.order += 1
        boardgame_number.boardgame_number_status = 'order'
    elif rental.order_status == 'canceled':
        boardgame_number.boardgame.in_stock += 1
        boardgame_number.boardgame.order -= 1
        boardgame_number.boardgame_number_status = 'in_stock'
    elif rental.order_status == 'accepted':
        if boardgame_number.boardgame_number_status == 'order':
            boardgame_number.boardgame.order -= 1
            boardgame_number.boardgame.rental += 1
            boardgame_number.boardgame_number_status = 'rental'
        if rental.rental_status == 'replied':
            if boardgame_number.boardgame_number_status == 'rental':
                boardgame_number.boardgame.in_stock += 1
                boardgame_number.boardgame.rental -= 1
                boardgame_number.boardgame_number_status = 'in_stock'
        
    boardgame_number.boardgame.total = boardgame_number.boardgame.in_stock + boardgame_number.boardgame.order + boardgame_number.boardgame.rental
    boardgame_number.boardgame.save()
    boardgame_number.save()
