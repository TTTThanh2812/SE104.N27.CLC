from django.shortcuts import render, get_object_or_404
from django.db import models
from django.db.models import Avg

from .models import Boardgame, BoardgameReviews#, Review, Rating, Category
# Create your views here.
def detail(request, bgid):
    # boardgame = get_object_or_404(Boardgame, bgid=bgid)
    boardgame = Boardgame.objects.get(bgid=bgid)
    # Giá thuê của boardgame 
    rental_price = boardgame.rental_price

    # Lấy tất cả review của boardgame 
    reviews = BoardgameReviews.objects.filter(boardgame=boardgame).order_by("-date")

    # Lấy trung bình rating của boardgame 
    average_rating = BoardgameReviews.objects.filter(boardgame=boardgame).aggregate(Avg('rating'))

    # if Rating.objects.filter(boardgame=boardgame).aggregate(Avg('stars'))['stars__avg'] != None:
    #     average_stars = int(Rating.objects.filter(boardgame=boardgame).aggregate(Avg('stars'))['stars__avg'])
    # else:
    #     average_stars = 0
    # draw_average_stars = range(0,average_stars)
    # draw_non_stars = range(0,5 - average_stars)
    related_boardgame = Boardgame.objects.filter(category=boardgame.category, boardgame_status="stocking").exclude(bgid=bgid)[0:3]
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
        # 'draw_average_s:tars':draw_average_stars,
        # 'draw_non_stars':draw_non_stars,
        'related_boardgame':related_boardgame,
        # 'related_boardgame_rating':related_boardgame_rating,
    }

    return render(request, 'boardgame/detail.html', context)

    