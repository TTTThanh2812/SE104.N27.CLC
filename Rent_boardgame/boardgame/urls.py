from django.urls import path

from . import views

app_name = 'boardgame'

urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),
]
