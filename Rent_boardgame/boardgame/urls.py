from django.urls import path
from boardgame import views

app_name = 'boardgame'

urlpatterns = [
    # detail boardgame
    path("detail/<str:boardgame_id>/", views.detail, name='detail'),
    path('search/', views.search_view, name='search'),
]