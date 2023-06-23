from django.contrib import admin

from boardgame.models import Category, Version, Author, Producer, Boardgame, BoardgameImages, BoardgameNumbers, BoardgameReviews

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'cid']

class VersionAdmin(admin.ModelAdmin):
    list_display = ['title', 'vid']

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['title', 'aid']

class ProducerAdmin(admin.ModelAdmin):
    list_display = ['title', 'pid']

class BoardgameImagesAdmin(admin.TabularInline):
    model = BoardgameImages

class BoardgameNumbersAdmin(admin.TabularInline):
    model = BoardgameNumbers

class BoardgameAdmin(admin.ModelAdmin):
    inlines = [BoardgameImagesAdmin, BoardgameNumbersAdmin]
    list_display = ['user', 'title', 'category', 'version', 'boardgame_image', 'price', 'boardgame_status', 'in_stock', 'rental', 'total']

class BoardgameReviewsAdmin(admin.ModelAdmin):
    list_display = ['user', 'boardgame', 'review', 'rating']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Producer, ProducerAdmin)
admin.site.register(Boardgame, BoardgameAdmin)
admin.site.register(BoardgameReviews, BoardgameReviewsAdmin)