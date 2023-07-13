from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db import models
from django.db.models import Avg
from boardgame.forms import BoardgameReviewForm
from django.core.paginator import Paginator
from django.db.models import F, DecimalField, ExpressionWrapper

from .models import Boardgame, BoardgameReviews, Category, Version, Author, Producer
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

def filter_boardgames(boardgames, filters):
    category = filters.get('category')
    version = filters.get('version')
    age_rating = filters.get('age_rating')
    people = filters.get('people')
    play_time = filters.get('play_time')
    author = filters.get('author')
    producer = filters.get('producer')
    publication_year = filters.get('publication_year')
    rental_price = filters.get('rental_price')
    rating = filters.get('rating')

    if category:
        boardgames = boardgames.filter(category__title=category)
    if version:
        boardgames = boardgames.filter(version__title=version)
    if age_rating:
        boardgames = boardgames.filter(age_rating=age_rating)
    if people:
        min_people, max_people = people.split(',')
        boardgames = boardgames.filter(people__gte=min_people, people__lte=max_people)
    if play_time:
        play_time_parts = play_time.split('-')
        if len(play_time_parts) == 2:
            min_play_time = int(play_time_parts[0])
            max_play_time = int(play_time_parts[1])
            boardgames = boardgames.filter(play_time__gte=min_play_time, play_time__lte=max_play_time)
    if author:
        boardgames = boardgames.filter(author__title=author)    
    if producer:
        boardgames = boardgames.filter(producer__title=producer)  
    if publication_year:
        min_publication_year, max_publication_year = publication_year.split(',')
        boardgames = boardgames.filter(publication_year__gte=min_publication_year, publication_year__lte=max_publication_year)
    if rental_price:
        min_price, max_price = rental_price.split('-')

        # Tính toán giá thuê
        rental_price_min = ExpressionWrapper(F('price') * 0.1, output_field=DecimalField())
        rental_price_max = ExpressionWrapper(F('price') * 0.1, output_field=DecimalField())

        # Lọc theo giá thuê
        boardgames = boardgames.annotate(rental_price_min=rental_price_min, rental_price_max=rental_price_max)
        boardgames = boardgames.filter(rental_price_min__gte=min_price, rental_price_max__lte=max_price)
    if rating:
        boardgames = boardgames.filter(reviews__rating=int(rating))
    return boardgames

def search_view(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        sort_by = request.GET.get('sort_by', '')
        filters = {
            'category': request.GET.get('category', None),
            'version': request.GET.get('version', None),
            'people': request.GET.get('people', None),
            'age_rating': request.GET.get('age_rating', None),
            'play_time': request.GET.get('play_time', None),
            'author': request.GET.get('author', None),
            'producer': request.GET.get('producer', None),
            'publication_year': request.GET.get('publication_year', None),
            'rental_price': request.GET.get('rental_price', None),
            'rating': request.GET.get('rating', None),
        }

        # Tìm kiếm boardgame
        boardgames = search_boardgames(query)

        # Sắp xếp boardgame
        if sort_by:
            boardgames = sort_boardgames(boardgames, sort_by)

        # Lọc boardgame 
        boardgames = filter_boardgames(boardgames, filters)
        categorys = Category.objects.all()
        versions = Version.objects.all()
        age_rating_choices = Boardgame.AGE_RATINGS
        authors = Author.objects.all()
        producers = Producer.objects.all()

        context = {
            'boardgames': boardgames,
            'query': query,
            'sort_by': sort_by,
            'filters': filters,
            'categorys': categorys,
            'versions': versions,
            'age_rating_choices': age_rating_choices,
            'authors': authors,
            'producers': producers,
        }

        return render(request, 'boardgame/search.html', context)