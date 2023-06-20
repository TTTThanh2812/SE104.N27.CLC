from django.contrib.auth import views as auth_views
from django.urls import path

from core import views
from .forms import SignInForm

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('allCategories/', views.allCategories, name='allCategories'),
    path('category/<int:category_mstl>/', views.category_view, name='category'),

]