from django.urls import path
from rent import views

app_name = 'rent'

urlpatterns = [
    path('request_rent_boardgame/<bgid>/', views.request_rent_boardgame, name='request_rent_boardgame'),
    path('rent_success/', views.rent_success, name='rent_success'),
    path('add-to-cart/<bgid>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart_item/<cart_item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove_from_cart/<cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('request_rent_cart/', views.request_rent_cart, name='request_rent_cart'),
]
