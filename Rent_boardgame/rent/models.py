from django.db import models
from userauths.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from notifications.signals import notify
from boardgame.models import BoardgameNumbers

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

class RentBoardgame(models.Model):
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

    rid = models.CharField(primary_key=True, max_length=20, unique=True)
    renter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    rental_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    deposit_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    penalty_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)  
    boardgames = models.ManyToManyField(BoardgameNumbers, through='RentBoardgameItem', related_name='rent_boardgames')

    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    rental_status = models.CharField(max_length=20, choices=RENTAL_STATUS_CHOICES, blank=True, null=True)

    def update_rental_status(self):
        now = timezone.now().date()
        if self.rental_status == 'active' and now > self.end_date:
            self.rental_status = 'expired'

    def update_boardgame_numbers(self):
        if self.order_status == 'canceled':
            for rent_item in self.items.all():
                if rent_item.boardgame_number:
                    boardgame_number = rent_item.boardgame_number
                    boardgame_number.boardgame.in_stock += rent_item.quantity
                    boardgame_number.boardgame.order -= rent_item.quantity
                    boardgame_number.boardgame_number_status = 'in_stock'
                    boardgame_number.boardgame.total = (
                        boardgame_number.boardgame.in_stock +
                        boardgame_number.boardgame.order +
                        boardgame_number.boardgame.rental
                    )
                    boardgame_number.save()  
                    boardgame_number.boardgame.save()  
            # print('order_status = canceled')
            return boardgame_number.boardgame, boardgame_number
        elif self.order_status == 'accepted':
            rental_status_active = False
            for rent_item in self.items.all():
                if rent_item.boardgame_number:
                    boardgame_number = rent_item.boardgame_number
                    if boardgame_number.boardgame_number_status == 'order':
                        boardgame_number.boardgame.order -= rent_item.quantity
                        boardgame_number.boardgame.rental += rent_item.quantity
                        boardgame_number.boardgame_number_status = 'rental'
                        rental_status_active = True
                        # print('order_status = accepted và boardgame_number_status = order')
                        # print(f'rent_item.quantity = {rent_item.quantity}')
                        # print(f'boardgame_number.boardgame.in_stock sau = {boardgame_number.boardgame.in_stock}')
                        # print(f'boardgame_number.boardgame.rental sau = {boardgame_number.boardgame.rental}')
                    if self.rental_status == 'replied':  
                        if boardgame_number.boardgame_number_status == 'rental':
                            boardgame_number.boardgame.rental -= rent_item.quantity
                            boardgame_number.boardgame.in_stock += rent_item.quantity
                            boardgame_number.boardgame_number_status = 'in_stock'
                        #     print('boardgame_number_status = rental')
                        #     print(f'rent_item.quantity = {rent_item.quantity}')
                        #     print(f'boardgame_number.boardgame.in_stock sau = {boardgame_number.boardgame.in_stock}')
                        #     print(f'boardgame_number.boardgame.rental sau = {boardgame_number.boardgame.rental}')
                        # print('order_status = accepted và rental_status = replied')

                    boardgame_number.boardgame.total = (
                        boardgame_number.boardgame.in_stock +
                        boardgame_number.boardgame.order +
                        boardgame_number.boardgame.rental
                    )
                    boardgame_number.save()  
                    boardgame_number.boardgame.save()  
                    # print(f'boardgame_number.boardgame sau lưu = {boardgame_number.boardgame.in_stock}, {boardgame_number.boardgame.order}, {boardgame_number.boardgame.rental}')
                    # print(f'boardgame_number sau lưu = {boardgame_number.boardgame_number_status}')
            
            if rental_status_active:
                self.rental_status = 'active'
                self.save()

            return boardgame_number.boardgame, boardgame_number
        

    def save(self, *args, **kwargs):
        if not self.rid:
            last_rent = RentBoardgame.objects.order_by('-rid').first()
            if last_rent:
                last_rid_number = int(last_rent.rid[4:])
                new_rid_number = last_rid_number + 1
                self.rid = f'rent{new_rid_number:02}'
            else:
                self.rid = 'rent01'
        self.update_boardgame_numbers()
        self.update_rental_status()
        super(RentBoardgame, self).save(*args, **kwargs)

        self.rental_price = sum(item.rental_price for item in self.items.all())
        self.deposit_price = float(self.rental_price) * 0.5
        self.total_price = float(self.rental_price) + float(self.deposit_price)
        
        super(RentBoardgame, self).save(update_fields=['rental_price', 'deposit_price', 'total_price'])
        

    def __str__(self):
        return f"{self.renter.username} - {self.start_date} to {self.end_date} - {self.rid}"

class RentBoardgameItem(models.Model):
    rent_boardgame = models.ForeignKey(RentBoardgame, on_delete=models.CASCADE, related_name='items')
    boardgame_number = models.ForeignKey(BoardgameNumbers, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    rental_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.rental_price = int(self.boardgame_number.boardgame.price) * 0.1 * self.quantity
        super(RentBoardgameItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.rent_boardgame} - {self.boardgame_number}"

    # @property
    # def rental_price(self):
    #     return self.boardgame_number.boardgame.price

