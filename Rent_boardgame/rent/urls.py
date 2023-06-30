from django.urls import path
from rent import views

app_name = 'rent'

urlpatterns = [
    path('request_rent_boardgame/<bgid>/', views.request_rent_boardgame, name='request_rent_boardgame'),
    path('rent_success/', views.rent_success, name='rent_success'),
]
