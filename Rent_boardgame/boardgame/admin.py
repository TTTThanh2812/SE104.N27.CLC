from django.contrib import admin

from .models import Category, Version, BoardGame, Rating, Review

admin.site.register(Category)
admin.site.register(Version)
admin.site.register(BoardGame)
admin.site.register(Rating)
admin.site.register(Review)