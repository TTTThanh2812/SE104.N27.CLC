from django.shortcuts import render, redirect
from django.db import models
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse

from boardgame.models import Category, Boardgame, Version, Author, Producer
from userauths.models import User
from django.contrib.auth.forms import PasswordChangeForm
from core.forms import UserProfileForm

# from .models import UserProfile

# Create your views here.
def home(request):
    categories = Category.objects.all()[0:3]
    top_boardgames = Boardgame.objects.annotate(avg_rating=models.Avg('reviews__rating')).order_by('-avg_rating')[:3]
    for t_boardgame in top_boardgames:
        most_recent_review = t_boardgame.reviews.order_by('-date').first()
        t_boardgame.most_recent_comment = most_recent_review

    return render(request, 'core/home.html', {
        'categories': categories,
        'top_boardgames': top_boardgames,
    })

def contact(request):
    return render(request, 'core/contact.html')

def allCategories(request):
    categories = Category.objects.all()
    return render(request, 'core/allCategories.html',{
        'categories': categories,
    })

def category_view(request, cid):
    category = Category.objects.get(cid=cid)
    boardgames = Boardgame.objects.filter(category=category)
    versions = Version.objects.all()
    age_rating_choices = Boardgame.AGE_RATINGS
    authors = Author.objects.all()
    producers = Producer.objects.all()

    
    return render(request, 'core/category.html', {
        'category': category,
        'boardgames': boardgames,
        'versions': versions,
        'age_rating_choices':age_rating_choices,
        'authors': authors,
        'producers': producers,
    })

@login_required
def account(request):
    user =  User.objects.get(user_id=request.user.user_id)
    context = {
        'user': user
    }
    return render(request, 'core/account.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Cập nhật session auth hash để tránh đăng xuất người dùng
            messages.success(request, 'Mật khẩu đã được thay đổi thành công!')
            return redirect(reverse('core:account'))
        else:
            if 'old_password' in form.errors:
                messages.error(request, 'Mật khẩu cũ không đúng.')
            if 'new_password2' in form.errors:
                messages.error(request, 'Mật khẩu xác nhận không khớp với mật khẩu mới.')
    else:
        form = PasswordChangeForm(user=request.user)
    
    context = {
        'form': form
    }
    return render(request, 'core/change_password.html', context)

@login_required
def edit_infomation(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thông tin cá nhân đã được cập nhật thành công!')
            return redirect(reverse('core:account'))
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form
    }
    return render(request, 'core/edit_infomation.html', context)