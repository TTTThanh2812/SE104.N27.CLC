from django.contrib import admin
from rent.models import RentBoardgame

class RentBoardgameAdmin(admin.ModelAdmin):
    list_display = ['renter', 'boardgame_title', 'rid', 'boardgame_numbers', 'order_status', 'rental_status']
    list_filter = ['renter', 'boardgame_numbers__boardgame__title', 'order_status', 'rental_status']
    list_editable = ['order_status', 'rental_status']
    search_fields = ['renter__username', 'boardgame_numbers__boardgame__title']
    # fields = ['renter', 'boardgame_numbers', 'start_date', 'end_date', 'rental_price', 'deposit_price', 'total_price', 'penalty_price']
    fieldsets = [
        ('Rent Information', {
            'fields': ('renter', 'boardgame_numbers', 'start_date', 'end_date', 'created_at', 'order_status', 'rental_status')
        }),
        ('Price', {
            'fields': ('rental_price', 'deposit_price', 'total_price', 'penalty_price')
        }),
    ]
    readonly_fields = ['renter', 'boardgame_numbers', 'start_date', 'end_date', 'rental_price', 'deposit_price', 'total_price']

    def boardgame_title(self, obj):
        return obj.boardgame_numbers.boardgame.title
    def boardgame_number(self, obj):
        return obj.boardgame_numbers.bgnid    

    boardgame_title.short_description = 'Boardgame Title'

admin.site.register(RentBoardgame, RentBoardgameAdmin)
