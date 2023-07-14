from django.shortcuts import render, redirect, get_object_or_404
from rent.models import RentBoardgame
from rent.forms import RentBoardgameForm
from boardgame.models import Boardgame
from django.contrib import messages

def request_rent_boardgame(request, bgid):
    boardgame = get_object_or_404(Boardgame, bgid=bgid)
    if request.method == 'POST':
        rent_form = RentBoardgameForm(request.POST)
        if rent_form.is_valid():
            rent_request = rent_form.save(commit=False)
            rent_request.renter = request.user
            boardgame_number = boardgame.boardgame_numbers.filter(boardgame_number_status='in_stock').first()
            rent_request.boardgame_numbers = boardgame_number
            
            start_date = rent_request.start_date
            end_date = rent_request.end_date
            rental_days = (end_date - start_date).days
            # Tính toán giá thuê, giá cọc, tổng tiền phải trả
            rental_price_per_day = float(boardgame_number.boardgame.price) * 0.1
            rental_price = rental_price_per_day * rental_days
            # rental_price = rent_request.calculate_rental_price()
            deposit_price = rental_price * 0.5
            total_price = rental_price + deposit_price

            rent_request.rental_price = rental_price
            rent_request.deposit_price = deposit_price
            rent_request.total_price = total_price

            # Kiểm tra điều kiện thuê
            previous_rent = RentBoardgame.objects.filter(renter=request.user).order_by('-end_date').last()
            if previous_rent:
                if previous_rent.end_date == rent_request.start_date:
                    # Ngày kết thúc boardgame trước đó trùng với ngày bắt đầu boardgame yêu cầu
                    # Gửi yêu cầu thuê thành công
                    rent_request.save()
                    messages.success(request, "Gửi yêu cầu thuê thành công.")
                    return redirect('rent:rent_success')
                elif previous_rent.end_date > rent_request.start_date:
                    # Ngày kết thúc boardgame trước đó lớn hơn ngày bắt đầu boardgame yêu cầu
                    # Xuất thông báo yêu cầu thuê không thành công
                    messages.error(request, "Yêu cầu thuê không thành công.")
                    return redirect('rent:request_rent_boardgame', bgid=bgid)
            rent_request.save()
            messages.success(request, "Gửi yêu cầu thuê thành công.")
            return redirect('rent:rent_success')
    else:
        rent_form = RentBoardgameForm()
        print(rent_form.errors)

    context = {
        'rent_form': rent_form,
        'boardgame': boardgame,
    }
    return render(request, "rent/request_rent_boardgame.html", context)

def rent_success(request):
    rental_requests = RentBoardgame.objects.filter(renter=request.user)
    context = {
        'rental_requests': rental_requests
    }
    return render(request, "rent/rent_success.html", context)
