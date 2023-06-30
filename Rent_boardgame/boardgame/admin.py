from django.contrib import admin

from boardgame.models import Category, Version, Author, Producer, Boardgame, BoardgameImages, BoardgameNumbers, BoardgameReviews

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'cid']
    search_fields = ['title']

class VersionAdmin(admin.ModelAdmin):
    list_display = ['title', 'vid']
    search_fields = ['title']

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['title', 'aid']
    search_fields = ['title']

class ProducerAdmin(admin.ModelAdmin):
    list_display = ['title', 'pid']
    search_fields = ['title']

class BoardgameImagesAdmin(admin.TabularInline):
    model = BoardgameImages

class BoardgameNumbersAdmin(admin.TabularInline):
    model = BoardgameNumbers

class BoardgameAdmin(admin.ModelAdmin):
    inlines = [BoardgameImagesAdmin, BoardgameNumbersAdmin]
    list_display = ['user', 'title', 'category', 'version', 'boardgame_image', 'price', 'boardgame_status', 'in_stock', 'rental', 'total']
    search_fields = ['title','category', 'version', 'boardgame_status']

class BoardgameReviewsAdmin(admin.ModelAdmin):
    list_display = ['user', 'boardgame', 'review', 'rating']
    search_fields = ['boardgame__title', 'rating']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Producer, ProducerAdmin)
admin.site.register(Boardgame, BoardgameAdmin)
admin.site.register(BoardgameReviews, BoardgameReviewsAdmin)