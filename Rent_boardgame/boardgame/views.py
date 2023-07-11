from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db import models
from django.db.models import Avg
from boardgame.forms import BoardgameReviewForm
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Boardgame, BoardgameReviews#, Review, Rating, Category
# Create your views here.
def detail(request, boardgame_id):
    # boardgame = get_object_or_404(Boardgame, bgid=bgid)
    boardgame = Boardgame.objects.get(bgid=boardgame_id)
    # Giá thuê của boardgame 
    rental_price = boardgame.rental_price

    # Xử lý submit form thêm review từ người thuê
    if request.method == 'POST':
        review_form = BoardgameReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.boardgame = boardgame
            review.save()
            review_form = BoardgameReviewForm()  # Reset form sau khi lưu thành công
    else:
        review_form = BoardgameReviewForm()

    # Lấy tất cả review của boardgame 
    reviews = BoardgameReviews.objects.filter(boardgame=boardgame).order_by("-date")
    

    # phân trang review
    paginator = Paginator(reviews, 5)  # Số lượng review trên mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Lấy trung bình rating của boardgame 
    average_rating = BoardgameReviews.objects.filter(boardgame=boardgame).aggregate(Avg('rating'))

    # draw_average_stars = range(0,average_stars)
    # draw_non_stars = range(0,5 - average_stars)
    related_boardgame = Boardgame.objects.filter(category=boardgame.category, boardgame_status="stocking").exclude(bgid=boardgame_id)[0:3]
    # related_boardgame_rating = []
    # for relate_bg_rating in related_boardgame:
    #     total_comments = Review.objects.filter(boardgame=relate_bg_rating).exclude(comment='').count()
    #     if Rating.objects.filter(boardgame=relate_bg_rating).exclude(stars=None).aggregate(models.Avg('stars'))['stars__avg'] != None:
    #         average_stars = int(Rating.objects.filter(boardgame=relate_bg_rating).exclude(stars=None).aggregate(models.Avg('stars'))['stars__avg'])
    #     else:
    #         average_stars = 0
    #     draw_average_stars = range(0,average_stars)
    #     draw_non_stars = range(0,5 - average_stars)
    #     related_boardgame_rating.append({'boardgame': relate_bg_rating, 
    #                                      'total_comments': total_comments,
    #                                      'average_stars': average_stars,
    #                                      'draw_average_stars':draw_average_stars,
    #                                      'draw_non_stars': draw_non_stars,
    #                                     })
    
    context ={
        'boardgame': boardgame,
        'rental_price':rental_price,
        'reviews':reviews,
        'average_rating':average_rating,
        'review_form': review_form,
        'page_obj': page_obj,
        # 'draw_average_stars':draw_average_stars,
        # 'draw_non_stars':draw_non_stars,
        'related_boardgame':related_boardgame,
        # 'related_boardgame_rating':related_boardgame_rating,
    }

    return render(request, 'boardgame/detail.html', context)

def search_boardgames(query):
    boardgames = Boardgame.objects.filter(title__icontains=query)
    return boardgames

def sort_boardgames(boardgames, sort_by):
    if sort_by == 'price_asc':
        boardgames = boardgames.order_by('price')
    elif sort_by == 'price_desc':
        boardgames = boardgames.order_by('-price')
    return boardgames

def search_view(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        sort_by = request.GET.get('sort_by', '')

        # Tìm kiếm boardgame
        boardgames = search_boardgames(query)

        # Sắp xếp boardgame
        if sort_by:
            boardgames = sort_boardgames(boardgames, sort_by)

        context = {
            'boardgames': boardgames,
            'query': query,
            'sort_by': sort_by,
        }

        return render(request, 'boardgame/search.html', context)