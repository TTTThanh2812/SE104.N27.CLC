# models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    MSHK = models.IntegerField(primary_key=True)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    point = models.IntegerField(default=0)

    
    def save(self, *args, **kwargs):
        if not self.MSHK:
            self.MSHK = generate_mshk()
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.MSHK)

def generate_mshk():
        # Logic để tạo giá trị MSHK duy nhất và tự động tăng dần 8 chữ số
        # Ví dụ: tạo giá trị từ 00000001 đến 99999999
        # Bạn có thể sử dụng random hoặc logic phù hợp để tạo giá trị MSHK
        # Trong ví dụ dưới đây, tôi sử dụng hàm count() để tìm số lượng người dùng hiện có
        # và tăng giá trị lên một để tạo giá trị tiếp theo
        last_user_profile = UserProfile.objects.last()
        if last_user_profile:
            return last_user_profile.MSHK + 1
        return 1