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
    extra = 0

class BoardgameNumbersAdmin(admin.TabularInline):
    model = BoardgameNumbers
    extra = 0
    fields = ['bgnid', 'boardgame_number_status', 'description', 'date']
    readonly_fields = ['bgnid']

class BoardgameAdmin(admin.ModelAdmin):
    inlines = [BoardgameImagesAdmin, BoardgameNumbersAdmin]
    list_display = ['title', 'category', 'version', 'boardgame_image', 'price', 'boardgame_status', 'in_stock', 'order', 'rental', 'total']
    list_filter = ['title', 'category', 'version', 'boardgame_status']
    # search_fields = ['title','category', 'version', 'boardgame_status']
    ordering = ['price', 'in_stock', 'order', 'rental', 'total']
    fieldsets = [
        ('Boardgame Information', {
            'fields': ('bgid', 'title', 'category', 'version', 'author', 'producer', 'publication_year')
        }),
        ('Game Details', {
            'fields': ('image', 'description', 'rule', 'age_rating', 'people', 'play_time', 'price')
        }),
        ('Availability', {
            'fields': ('boardgame_status', 'in_stock', 'order', 'rental', 'total')
        }),
        ('Additional Information', {
            'fields': ('user', 'date')
        }),
    ]
    readonly_fields = ['bgid', 'boardgame_status', 'in_stock', 'order', 'rental', 'total']

class BoardgameReviewsAdmin(admin.ModelAdmin):
    list_display = ['user', 'boardgame', 'review', 'rating']
    search_fields = ['boardgame__title', 'rating']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Producer, ProducerAdmin)
admin.site.register(Boardgame, BoardgameAdmin)
admin.site.register(BoardgameReviews, BoardgameReviewsAdmin)