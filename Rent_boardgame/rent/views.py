from django.shortcuts import render, redirect, get_object_or_404
from rent.models import RentBoardgame, RentBoardgameItem, Cart
from rent.forms import RentBoardgameForm, RentBoardgameCartForm
from boardgame.models import Boardgame, BoardgameNumbers
from django.contrib import messages
from decimal import Decimal

def add_to_cart(request, bgid):
    boardgame = get_object_or_404(Boardgame, bgid=bgid)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('userauths:sign_in')

        cart_item, created = Cart.objects.get_or_create(user=request.user, boardgame=boardgame)

        if created:
            cart_item.quantity = 1
        else:
            cart_item.quantity += 1

        cart_item.total_rental_price = cart_item.boardgame.rental_price
        cart_item.save()
        return redirect('rent:cart')

    return redirect('boardgame:detail', boardgame.bgid)

def update_cart_item(request, cart_item_id):
    cart_item = Cart.objects.get(id=cart_item_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            cart_item.quantity -= 1
            if cart_item.quantity < 1:
                cart_item.quantity = 1

        cart_item.total_rental_price = cart_item.rental_price * cart_item.quantity
        cart_item.save()

    return redirect('rent:cart')

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id)
    cart_item.delete()
    return redirect('rent:cart')

def view_cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    context = {
        'cart_items': cart_items
    }
    return render(request, 'rent/cart.html', context)

def request_rent_boardgame(request, bgid):
    boardgame = get_object_or_404(Boardgame, bgid=bgid)

    if request.method == 'POST':
        rent_form = RentBoardgameForm(request.POST)  # Pass None for direct rental
        if rent_form.is_valid():
            start_date = rent_form.cleaned_data['start_date']
            end_date = rent_form.cleaned_data['end_date']
            quantity = rent_form.cleaned_data['quantity']

            # Check if the boardgame is available for rent
            if boardgame.boardgame_status == 'out_of_stock':
                messages.error(request, 'This boardgame is currently out of stock.')
                return redirect('boardgame:detail', boardgame.bgid)

            if quantity > boardgame.in_stock:
                messages.error(request, 'Not enough boardgames available for rent.')
                return redirect('boardgame:detail', boardgame.bgid)

            if request.user.is_authenticated:
                # Rent the boardgame directly
                rent_boardgame = RentBoardgame.objects.create(renter=request.user, start_date=start_date, end_date=end_date)

                for _ in range(quantity):
                    boardgame_number = BoardgameNumbers.objects.filter(boardgame=boardgame, boardgame_number_status='in_stock').first()
                    if not boardgame_number:
                        messages.error(request, 'Not enough boardgames available for rent.')
                        return redirect('boardgame:detail', boardgame.bgid)

                    rent_item = RentBoardgameItem.objects.create(rent_boardgame=rent_boardgame, boardgame_number=boardgame_number)
                    rent_item.rental_price = boardgame_number.boardgame.rental_price()
                    rent_item.save()

                    boardgame_number.boardgame.in_stock -= 1
                    boardgame_number.boardgame.order += 1
                    boardgame_number.boardgame_number_status = 'order'
                    boardgame_number.boardgame.total = boardgame_number.boardgame.in_stock + boardgame_number.boardgame.order + boardgame_number.boardgame.rental
                    boardgame_number.boardgame.save()
                    boardgame_number.save()

                rent_boardgame.start_date = start_date
                rent_boardgame.end_date = end_date
                rent_boardgame.save()
                

                messages.success(request, f'Successfully rented {quantity} boardgame(s).')
                return redirect('rent:rent_success')
    else:
        rent_form = RentBoardgameForm()
        print(rent_form.errors)

    context = {
        'boardgame': boardgame,
        'rent_form': rent_form,
    }
    return render(request, 'rent/request_rent_boardgame.html', context)

# @login_required
def request_rent_cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    if request.method == 'POST':
        selected_cart_item_ids = request.POST.getlist('boardgames[]')

        # Filter out any empty values from the selected_cart_item_ids list
        selected_cart_item_ids = [cart_item_id for cart_item_id in selected_cart_item_ids if cart_item_id]

        cart_items = Cart.objects.filter(user=request.user, id__in=selected_cart_item_ids)

        if cart_items:
            form = RentBoardgameCartForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                quantity = 0

                for cart_item in cart_items:
                    boardgame = cart_item.boardgame
                    if boardgame.boardgame_status == 'out_of_stock':
                        messages.error(request, 'This boardgame is currently out of stock.')
                        return redirect('rent:cart')

                    quantity += cart_item.quantity
                    if cart_item.quantity > boardgame.in_stock:
                        messages.error(request, 'Not enough boardgames available for rent.')
                        return redirect('rent:cart')
                    
                    if request.user.is_authenticated:
                        rent_boardgame = RentBoardgame.objects.create(renter=request.user, start_date=start_date, end_date=end_date)

                        for _ in range(cart_item.quantity):
                            boardgame_number = BoardgameNumbers.objects.filter(boardgame=boardgame, boardgame_number_status='in_stock').first()
                            if not boardgame_number:
                                messages.error(request, 'Not enough boardgames available for rent.')
                                return redirect('rent:cart')

                            rent_item = RentBoardgameItem.objects.create(rent_boardgame=rent_boardgame, boardgame_number=boardgame_number)
                            rent_item.rental_price = boardgame_number.boardgame.rental_price()
                            rent_item.save()

                            boardgame_number.boardgame.in_stock -= 1
                            boardgame_number.boardgame.order += 1
                            boardgame_number.boardgame_number_status = 'order'
                            boardgame_number.boardgame.total = boardgame_number.boardgame.in_stock + boardgame_number.boardgame.order + boardgame_number.boardgame.rental
                            boardgame_number.boardgame.save()
                            boardgame_number.save()
                
                cart_items.delete()
                rent_boardgame.start_date = start_date
                rent_boardgame.end_date = end_date
                rent_boardgame.save()

                messages.success(request, f'Successfully rented boardgame(s).')
                return redirect('rent:rent_success')
            else:
                # Invalid formset
                messages.error(request, 'Please fill in the required fields.')
        else:
            messages.error(request, 'Please select boardgames to rent.')
            return redirect('rent:cart')
    else:
        form = RentBoardgameCartForm()

    context = {
        'form': form,
        'cart_items': cart_items
    }
    return render(request, 'rent/request_rent_cart.html', context)
# def request_rent_cart(request):
#     if request.method == 'POST':
#         selected_boardgames = request.POST.getlist('boardgames[]')
#         cart_items = Cart.objects.filter(pk__in=selected_boardgames)
#         form = RentBoardgameForm(request.POST)
#         context = {
#             'form': form,
#             'cart_items': cart_items
#         }
#         return render(request, 'rent/request_rent_cart.html', context)
#     else:
#         return redirect('rent:cart')

def rent_success(request):
    rental_requests = RentBoardgame.objects.filter(renter=request.user)
    context = {
        'rental_requests': rental_requests
    }
    return render(request, "rent/rent_success.html", context)