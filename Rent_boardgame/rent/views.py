from django.shortcuts import render, redirect, get_object_or_404
from rent.models import RentBoardgame
from rent.forms import RentBoardgameForm
from boardgame.models import Boardgame
from decimal import Decimal

def request_rent_boardgame(request, bgid):
    boardgame = get_object_or_404(Boardgame, bgid=bgid)
    if request.method == 'POST':
        rent_form = RentBoardgameForm(request.POST)
        if rent_form.is_valid():
            rent_request = rent_form.save(commit=False)
            rent_request.renter = request.user
            boardgame_number = boardgame.boardgame_numbers.filter(boardgame_number_status='in_stock').first()
            rent_request.boardgame_numbers = boardgame_number
            rent_request.rental_price = rent_request.calculate_rental_price()
            rent_request.save()
            return redirect('rent:rent_success')
    else:
        rent_form = RentBoardgameForm()
        print(rent_form.errors)

    context = {
        'rent_form': rent_form,
    }
    return render(request, "rent/request_rent_boardgame.html", context)

def rent_success(request):
    rental_requests = RentBoardgame.objects.filter(renter=request.user)
    context = {
        'rental_requests': rental_requests
    }
    return render(request, "rent/rent_success.html", context)
