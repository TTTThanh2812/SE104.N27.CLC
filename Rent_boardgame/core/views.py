from django.shortcuts import render, redirect
from django.db import models
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required

from boardgame.models import Category, Boardgame#, Rating, Review
from userauths.models import User

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

    search_query = request.GET.get('search')
    if search_query:
        boardgames = boardgames.filter(name__icontains=search_query)

    sort_option = request.GET.get('sort')
    if sort_option == 'category':
        boardgames = boardgames.order_by('category')
    elif sort_option == 'people':
        boardgames = boardgames.order_by('people')
    elif sort_option == 'age':
        boardgames = boardgames.order_by('age_rating')
    elif sort_option == 'time':
        boardgames = boardgames.order_by('play_time')
    elif sort_option == 'author':
        boardgames = boardgames.order_by('author')
    elif sort_option == 'producer':
        boardgames = boardgames.order_by('producer')
    elif sort_option == 'year':
        boardgames = boardgames.order_by('publication_year')
    elif sort_option == 'price':
        boardgames = boardgames.order_by('price')
    elif sort_option == 'rating':
        boardgames = boardgames.order_by('-average_rating')
    
    return render(request, 'core/category.html', {
        'category': category,
        'boardgames': boardgames,
    })

@login_required
def account(request):
    user =  User.objects.get(user_id=request.user.user_id)
    context = {
        'user': user
    }
    return render(request, 'core/account.html', context)
