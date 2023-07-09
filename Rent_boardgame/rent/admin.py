from django.contrib import admin
from rent.models import RentBoardgame

class RentBoardgameAdmin(admin.ModelAdmin):
    list_display = ['renter', 'boardgame_title', 'boardgame_rent_id']
    list_filter = ['order_status', 'rental_status']
    search_fields = ['renter__username', 'boardgame_numbers__boardgame__title']

    def boardgame_title(self, obj):
        return obj.boardgame_numbers.boardgame.title

    boardgame_title.short_description = 'Boardgame Title'

admin.site.register(RentBoardgame, RentBoardgameAdmin)
