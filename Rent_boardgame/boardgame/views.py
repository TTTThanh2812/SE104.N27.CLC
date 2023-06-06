from django.shortcuts import render, get_object_or_404

from .models import BoardGame
# Create your views here.
def detail(request, pk):
    boardgame = get_object_or_404(BoardGame, pk=pk)
    rental_price = boardgame.rental_price
    quantity_in_stock = boardgame.update_quantity_in_stock()
    related_boardgame = BoardGame.objects.filter(category=boardgame.category, is_sold=False).exclude(pk=pk)[0:3]
    return render(request, 'boardgame/detail.html', {
        'boardgame': boardgame,
        'rental_price':rental_price,
        'quantity_in_stock':quantity_in_stock,
        'related_boardgame':related_boardgame,
    })