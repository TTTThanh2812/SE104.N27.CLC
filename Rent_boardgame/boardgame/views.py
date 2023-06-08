from django.shortcuts import render, get_object_or_404
from django.db import models
from django.db.models import Avg

from .models import BoardGame, Review, Rating, Category
# Create your views here.
def detail(request, pk):
    boardgame = get_object_or_404(BoardGame, pk=pk)
    rental_price = boardgame.rental_price
    quantity_in_stock = boardgame.update_quantity_in_stock()
    total_comments = Review.objects.exclude(boardgame=boardgame).count()
    if Rating.objects.filter(boardgame=boardgame).aggregate(Avg('stars'))['stars__avg'] != None:
        average_stars = int(Rating.objects.filter(boardgame=boardgame).aggregate(Avg('stars'))['stars__avg'])
    else:
        average_stars = 0
    draw_average_stars = range(0,average_stars)
    draw_non_stars = range(0,5 - average_stars)
    related_boardgame = BoardGame.objects.filter(category=boardgame.category, is_sold=False).exclude(pk=pk)[0:3]
    related_boardgame_rating = []
    for relate_bg_rating in related_boardgame:
        total_comments = Review.objects.filter(boardgame=relate_bg_rating).exclude(comment='').count()
        if Rating.objects.filter(boardgame=relate_bg_rating).exclude(stars=None).aggregate(models.Avg('stars'))['stars__avg'] != None:
            average_stars = int(Rating.objects.filter(boardgame=relate_bg_rating).exclude(stars=None).aggregate(models.Avg('stars'))['stars__avg'])
        else:
            average_stars = 0
        draw_average_stars = range(0,average_stars)
        draw_non_stars = range(0,5 - average_stars)
        related_boardgame_rating.append({'boardgame': relate_bg_rating, 
                                         'total_comments': total_comments,
                                         'average_stars': average_stars,
                                         'draw_average_stars':draw_average_stars,
                                         'draw_non_stars': draw_non_stars,
                                        })
    return render(request, 'boardgame/detail.html', {
        'boardgame': boardgame,
        'rental_price':rental_price,
        'quantity_in_stock':quantity_in_stock,
        'total_comments':total_comments,
        'average_stars':average_stars,
        'draw_average_stars':draw_average_stars,
        'draw_non_stars':draw_non_stars,
        'related_boardgame':related_boardgame,
        'related_boardgame_rating':related_boardgame_rating,
    })
