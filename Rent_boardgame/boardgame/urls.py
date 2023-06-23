from django.urls import path
from boardgame import views

app_name = 'boardgame'

urlpatterns = [
    path("<bgid>/", views.detail, name='detail'),
]