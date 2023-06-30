from django.db import models
from userauths.models import User
# from boardgame.models import BoardgameNumbers
from django.utils import timezone

STATUS_CHOICES = [
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
    created_at = models.DateTimeField(default=timezone.now)  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rental_status = models.CharField(max_length=20, choices=RENTAL_STATUS_CHOICES, blank=True)
    
    class Meta:
        ordering = ['rid']

    def boardgame_rent_id(self):
        return f"{self.boardgame_numbers.boardgame.cid}{self.boardgame_numbers.boardgame.vid}{self.boardgame_numbers.bgid}{self.bgnid}"

    def calculate_rental_price(self):
        rental_days = (self.end_date - self.start_date).days
        rental_price_per_day = self.boardgame_numbers.boardgame.rental_price
        return rental_days * rental_price_per_day
    
    def is_expired(self):
        return self.rental_status == 'active' and self.end_date < timezone.now().date()

    def __str__(self):
        return f"{self.renter.username} - {self.boardgame_numbers.boardgame.title} - {self.rid}"

