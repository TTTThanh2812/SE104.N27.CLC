from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import random
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    # code = random.randint(10, 99)
    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Categories'

    def __str__(self): # Đổi tên category
        return f"{self.name}"
    
class Version(models.Model):
    name = models.CharField(max_length=255)
    # code = random.randint(10, 99)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Version'

    def __str__(self): 
        return f"{self.name}"
    
class BoardGame(models.Model):
    AGE_RATINGS = [
        ('G', 'Phổ biến'),
        ('7+', 'Trên 7 tuổi'),
        ('12+', 'Trên 12 tuổi'),
        ('16+', 'Trên 16 tuổi'),
        ('18+', 'Trên 18 tuổi'),
    ]
    STATUS_CHOICES = [
        ('rental', 'Rental'),
        ('in_stock', 'In Stock'),
    ]

    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    version = models.ForeignKey(Version, related_name='boardgames', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    rule = models.TextField(blank=True, null=True)
    
    age_rating = models.CharField(max_length=5, choices=AGE_RATINGS)
    people = models.CharField(max_length=100)
    play_time = models.CharField(max_length=50)
    price = models.FloatField()
    # rating = models.DecimalField(max_digits=3, decimal_places=1)
    image= models.ImageField(upload_to='item_images', blank=True, null=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    producer = models.CharField(max_length=255, null=True, blank=True)
    publication_year = models.FloatField( null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='in_stock')
    condition = models.TextField(blank=True, null=True)
    quantity_in_stock = models.PositiveIntegerField(default=1)
    quantity_rented = models.PositiveIntegerField(default=0)
    is_sold = models.BooleanField(default=False)
    rented_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self): # Đổi tên category
        return f"{self.name}"
    
    # Lựa chọn khoản giá trị 
    def set(self, min_value, max_value):
        self.people = f"{min_value}-{max_value}"
        self.play_time = f"{min_value}-{max_value}"
    def get_min_value(self):
        return int(self.people.split('-')[0])
    def get_max_value(self):
        return int(self.people.split('-')[1])
    
    # Giá thuê
    def rental_price(self):
        return int(self.price * 0.1)

    # Cập nhập số lượng hiện có
    def update_quantity_in_stock(self):
        total_quantity = BoardGame.objects.filter(name=self.name, category=self.category, version=self.version).count()
        self.quantity_in_stock = total_quantity
        self.save()

class Review(models.Model):
    boardgame = models.ForeignKey(BoardGame, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Review by {self.user.username} for {self.boardgame.name}'
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    boardgame = models.ForeignKey(BoardGame, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.boardgame.name} - {self.stars} stars"
    