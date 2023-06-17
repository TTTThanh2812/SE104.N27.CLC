from django.shortcuts import render, redirect
from django.db import models
from django.contrib.auth import logout

from django.contrib.auth.models import User
from boardgame.models import Category, BoardGame, Rating, Review

from .forms import SignUpForm, SignInForm
from .models import UserProfile

# Create your views here.
def home(request):
    boardgames = BoardGame.objects.filter(is_sold=False)[0:6] # Hiển thị ra tối đa bao nhiêu boardgame 
    categories = Category.objects.all()[0:2]
    boardgame_ratings = []
    for boardgame in boardgames:
        total_comments = Review.objects.filter(boardgame=boardgame).exclude(comment='').count()
        if Rating.objects.filter(boardgame=boardgame).exclude(stars=None).aggregate(models.Avg('stars'))['stars__avg'] != None:
            average_stars = int(Rating.objects.filter(boardgame=boardgame).exclude(stars=None).aggregate(models.Avg('stars'))['stars__avg'])
        else:
            average_stars = 0
        draw_average_stars = range(0,average_stars)
        draw_non_stars = range(0,5 - average_stars)
        # Lấy bình luận gần nhất của boardgame
        if Review.objects.filter(boardgame=boardgame).exclude(comment=''):
            latest_comment = Review.objects.filter(boardgame=boardgame).latest('created_at')
        # Lấy tên người bình luận
        comment_author_name = latest_comment.user.username
        # Lấy nội dung bình luận
        comment_content = latest_comment.comment
        # comment_created_at = latest_comment.created_at
        # Lấy ngày và giờ bình luận
        comment_date = latest_comment.created_at.date()
        comment_time = latest_comment.created_at.time()

        #MSBG
        msbg = boardgame.get_msbg()
        boardgame_ratings.append({'boardgame': boardgame, 
                                  'total_comments': total_comments,
                                  'average_stars': average_stars,
                                  'draw_average_stars':draw_average_stars,
                                  'draw_non_stars': draw_non_stars,
                                  'comment_author_name':comment_author_name,
                                  'comment_content':comment_content,
                                  'comment_date':comment_date,
                                  'comment_time':comment_time,
                                  })
    top_boardgames = BoardGame.objects.annotate(avg_rating=models.Avg('rating__stars')).order_by('-avg_rating')[:3]


    return render(request, 'core/home.html', {
        'categories': categories,
        'boardgames': boardgames,
        'boardgame_ratings':boardgame_ratings,
        'top_boardgames': top_boardgames,
    })

def contact(request):
    return render(request, 'core/contact.html')

def allCategories(request):
    boardgames = BoardGame.objects.filter(is_sold=False)[0:6] # Hiển thị ra tối đa bao nhiêu boardgame 
    categories = Category.objects.all()
    boardgame_ratings = []
    for boardgame in boardgames:
        total_comments = Review.objects.filter(boardgame=boardgame).exclude(comment='').count()
        if Rating.objects.filter(boardgame=boardgame).exclude(stars=None).aggregate(models.Avg('stars'))['stars__avg'] != None:
            average_stars = int(Rating.objects.filter(boardgame=boardgame).exclude(stars=None).aggregate(models.Avg('stars'))['stars__avg'])
        else:
            average_stars = 0
        draw_average_stars = range(0,average_stars)
        draw_non_stars = range(0,5 - average_stars)
        boardgame_ratings.append({'boardgame': boardgame, 
                                  'total_comments': total_comments,
                                  'average_stars': average_stars,
                                  'draw_average_stars':draw_average_stars,
                                  'draw_non_stars': draw_non_stars,
                                })
    return render(request, 'core/allCategories.html',{
        'categories': categories,
        'boardgames': boardgames,
        'boardgame_ratings':boardgame_ratings,
    })

def category_view(request, category_mstl):
    category = Category.objects.get(mstl=category_mstl)
    boardgames = BoardGame.objects.filter(category=category)
    boardgame_ratings = []
    for boardgame in boardgames:
        total_comments = Review.objects.filter(boardgame=boardgame).exclude(comment='').count()
        if Rating.objects.filter(boardgame=boardgame).exclude(stars=None).aggregate(models.Avg('stars'))['stars__avg'] != None:
            average_stars = int(Rating.objects.filter(boardgame=boardgame).exclude(stars=None).aggregate(models.Avg('stars'))['stars__avg'])
        else:
            average_stars = 0
        draw_average_stars = range(0,average_stars)
        draw_non_stars = range(0,5 - average_stars)
        boardgame_ratings.append({'boardgame': boardgame, 
                                  'total_comments': total_comments,
                                  'average_stars': average_stars,
                                  'draw_average_stars':draw_average_stars,
                                  'draw_non_stars': draw_non_stars,
                                })

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
        'boardgame_ratings':boardgame_ratings,
    })

def signUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            # username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            # profile = UserProfile.objects.create(
            #     user=username,
            #     email=email,
            #     # Các trường khác
            # )
            return redirect('/')
    else:
        form = SignUpForm()

    return render(request, 'core/signUp.html', {
        'form': form
    })

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('/')
    else:
        form = SignInForm()
    return render(request, 'signin.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('/')
