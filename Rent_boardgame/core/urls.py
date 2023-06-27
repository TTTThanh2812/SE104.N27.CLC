from django.contrib.auth import views as auth_views
from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    # path('contact/', views.contact, name='contact'),
    path('allCategories/', views.allCategories, name='allCategories'),
    path('category/<cid>/', views.category_view, name='category'),
    path('account/', views.account, name='account'),
    path('change_password/', views.change_password, name='change_password'),
    path('editInfomation/', views.editInfomation, name='editInfomation'),
]