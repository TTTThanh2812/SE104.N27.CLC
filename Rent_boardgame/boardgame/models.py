from django.db import models
from django.utils import timezone
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import random
# Create your models here.
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    title = models.CharField(max_length=100, default=None)
    cid = ShortUUIDField(unique=True, primary_key=True, prefix="cat", alphabet='1234567890', length=2, max_length=6)
    description = models.TextField(null=True, blank=True)
    # code = random.randint(10, 99)
    class Meta:
        verbose_name_plural = 'Category'

    def __str__(self): 
        return self.title

class Version(models.Model):
    title = models.CharField(max_length=100, default=None)
    vid = ShortUUIDField(unique=True, primary_key=True, prefix="ver", alphabet='1234567890', length=2, max_length=6)
    description = models.TextField(null=True, blank=True)
    # code = random.randint(10, 99)
    class Meta:
        verbose_name_plural = 'Version'

    def __str__(self): 
        return self.title

class Author(models.Model):
    title = models.CharField(max_length=100, default=None)
    aid = ShortUUIDField(unique=True, primary_key=True, prefix="author", alphabet='1234567890', length=2, max_length=6)
    description = models.TextField(null=True, blank=True)
    # code = random.randint(10, 99)
    class Meta:
        verbose_name_plural = 'Author'

    def __str__(self): 
        return self.title
    
class Producer(models.Model):
    title = models.CharField(max_length=100, default=None)
    pid = ShortUUIDField(unique=True, primary_key=True, prefix="producer", alphabet='1234567890', length=2, max_length=6)
    description = models.TextField(null=True, blank=True)
    # code = random.randint(10, 99)
    class Meta:
        verbose_name_plural = 'Producer'

    def __str__(self): 
        return self.title

AGE_RATINGS = (
        ('G', 'Phổ biến'),
        ('7+', 'Trên 7 tuổi'),
        ('12+', 'Trên 12 tuổi'),
        ('16+', 'Trên 16 tuổi'),
        ('18+', 'Trên 18 tuổi'),
    )
STATUS_BG = (
    ('out_of_stock', 'Boardgame này đã hết'),
    ('stocking', 'Boardgame này vẫn còn'),
)
class  Boardgame(models.Model):
    bgid = ShortUUIDField(unique=True, prefix="bg", alphabet='1234567890', length=2, max_length=6)
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=timezone.now)  

    category= models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    version = models.ForeignKey(Version, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="user_directory_path")
    description = models.TextField(null=True, blank=True, default="This is the boardgame")
    rule = models.TextField(null=True, blank=True, default="This is rule for boardgame")

    age_rating = models.CharField(choices=AGE_RATINGS, max_length=5, default="G")
    people = models.CharField(max_length=100)
    play_time = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=99999999999999, decimal_places=2)

    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    producer = models.ForeignKey(Producer, on_delete=models.SET_NULL, null=True, blank=True)
    publication_year = models.CharField(max_length=4, default="2000")

    boardgame_status = models.CharField(choices=STATUS_BG, max_length=20, default="out_of_stock")
    in_stock = models.PositiveIntegerField(default=0)
    rental = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Boardgame"

    def boardgame_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
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
        return float(self.price) * 0.1
    
    def get_average_rating(self):
        return self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
    
    def __str__(self):
        return self.title
    

class BoardgameImages(models.Model):
    image = models.ImageField(upload_to="boardgame-images")
    boardgame = models.ForeignKey(Boardgame, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=timezone.now)   

    class Meta:
        verbose_name_plural = "Boardgame Images"

STATUS_BGN = (
        ('rental', 'Rental'),
        ('in_stock', 'In Stock'),
)
class BoardgameNumbers(models.Model):
    bgnid = ShortUUIDField(unique=True, prefix="bgn", alphabet='1234567890', length=2, max_length=20)

    boardgame = models.ForeignKey(Boardgame, on_delete=models.CASCADE, related_name='boardgame_numbers', null=True)
    boardgame_number_status = models.CharField(choices=STATUS_BGN, max_length=20)
    
    description = models.TextField(null=True, blank=True, default="This is boardgame status")

    date = models.DateTimeField(default=timezone.now)   

    class Meta:
        verbose_name_plural = "Boardgame Numbers"

    def save(self, *args, **kwargs):
        if not self.bgnid:
            # Tạo bgnid tự động
            mstl = self.boardgame.category.cid
            mpb = self.boardgame.version.vid
            msbg = self.boardgame.bgid
            sequence_number = self.bgnid
            new_bgnid = f"{mstl}{mpb}{msbg}{sequence_number}"
            self.bgnid = new_bgnid

        super().save(*args, **kwargs)

@receiver(post_save, sender=BoardgameNumbers)
def update_boardgame_stats(sender, instance, **kwargs):
    boardgame = instance.boardgame
    boardgame_numbers = boardgame.boardgame_numbers.all()
    
    in_stock_count = boardgame_numbers.filter(boardgame_number_status='in_stock').count()
    rental_count = boardgame_numbers.filter(boardgame_number_status='rental').count()
    
    if in_stock_count == 0:
        boardgame.boardgame_status = 'out_of_stock'
    else:
        boardgame.boardgame_status = 'stocking'
    
    boardgame.in_stock = in_stock_count
    boardgame.rental = rental_count
    boardgame.total = boardgame.in_stock + boardgame.rental
    
    boardgame.save()

@receiver(post_delete, sender=BoardgameNumbers)
def update_boardgame_stats_on_delete(sender, instance, **kwargs):
    boardgame = instance.boardgame
    boardgame_numbers = boardgame.boardgame_numbers.all()
    
    in_stock_count = boardgame_numbers.filter(boardgame_number_status='in_stock').count()
    rental_count = boardgame_numbers.filter(boardgame_number_status='rental').count()
    
    if in_stock_count == 0:
        boardgame.boardgame_status = 'out_of_stock'
    else:
        boardgame.boardgame_status = 'stocking'
    
    boardgame.in_stock = in_stock_count
    boardgame.rental = rental_count
    boardgame.total = boardgame.in_stock + boardgame.rental
    
    boardgame.save()

RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)
class BoardgameReviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    boardgame = models.ForeignKey(Boardgame, on_delete=models.SET_NULL, null=True, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(default=timezone.now)   

    class Meta:
        verbose_name_plural = "Boardgame Reviews"
    
    def __str__(self):
        return self.boardgame.title
    
    def get_rating(self):
        return self.rating

    def get_username(self):
        return self.user.username