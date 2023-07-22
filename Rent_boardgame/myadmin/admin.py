from django.contrib import admin
from boardgame.models import Category, Version, Author, Producer, Boardgame, BoardgameImages, BoardgameNumbers, BoardgameReviews
from rent.models import RentBoardgame, RentBoardgameItem
from userauths.models import User
from django.db.models import Q
# from rent.forms import RentBoardgameItemForm
from django.forms.models import BaseInlineFormSet
from django import forms

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['cid', 'title']
    list_filter = ['title']
    readonly_fields = ['cid']

class VersionAdmin(admin.ModelAdmin):
    list_display = ['vid', 'title']
    list_filter = ['title']
    readonly_fields = ['vid']

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['aid', 'title']
    list_filter = ['title']
    readonly_fields = ['aid']

class ProducerAdmin(admin.ModelAdmin):
    list_display = ['pid', 'title']
    list_filter = ['title']
    readonly_fields = ['pid']

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
    def get_search_results(self, request, queryset, search_term):
        # Thực hiện tìm kiếm và trả về kết quả
        results = Boardgame.objects.filter(title__icontains=search_term)
        return results, False
    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Override phương thức change_view để sử dụng template search_results.html
        self.change_list_template = 'admin/search_results.html'
        return super().change_view(request, object_id, form_url, extra_context)

class BoardgameReviewsAdmin(admin.ModelAdmin):
    list_display = ['user', 'boardgame', 'display_review', 'rating', 'date']
    list_filter = ['boardgame', 'rating']
    readonly_fields = ['user', 'boardgame', 'review', 'rating', 'date']
    def display_review(self, obj):
        MAX_LENGTH = 50  
        if len(obj.review) > MAX_LENGTH:
            return obj.review[:MAX_LENGTH] + '...'  
        return obj.review
    display_review.short_description = 'Review'

# class RentBoardgameAdmin(admin.ModelAdmin):
#     list_display = ['renter', 'boardgame_title', 'rid', 'order_status', 'rental_status']
#     list_filter = ['renter', 'order_status', 'rental_status']
#     list_editable = ['order_status', 'rental_status']
#     search_fields = ['renter__username', 'boardgame_numbers__boardgame__title']
#     # fields = ['renter', 'boardgame_numbers', 'start_date', 'end_date', 'rental_price', 'deposit_price', 'total_price', 'penalty_price']
#     fieldsets = [
#         ('Rent Information', {
#             'fields': ('renter', 'boardgame_numbers', 'start_date', 'end_date', 'created_at', 'order_status', 'rental_status')
#         }),
#         ('Price', {
#             'fields': ('rental_price', 'deposit_price', 'total_price', 'penalty_price')
#         }),
#     ]
#     readonly_fields = ['renter', 'start_date', 'end_date', 'rental_price', 'deposit_price', 'total_price']

#     def boardgame_title(self, obj):
#         return obj.boardgame_numbers.boardgame.title
#     def boardgame_number(self, obj):
#         return obj.boardgame_numbers.bgnid    

#     boardgame_title.short_description = 'Boardgame Title'

class RentBoardgameItemForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = RentBoardgameItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Fetch the related BoardgameNumbers instance if it exists
        try:
            boardgame_number = self.instance.boardgame_number
            if boardgame_number:
                # Set initial value for the description field
                self.initial['description'] = boardgame_number.description
        except RentBoardgameItem.boardgame_number.RelatedObjectDoesNotExist:
            pass

class RentBoardgameItemInlineFormSet(BaseInlineFormSet):
    def save_m2m(self):
        # Override the save_m2m method to handle ManyToMany fields
        pass

class RentBoardgameItemInline(admin.TabularInline):
    model = RentBoardgameItem
    form = RentBoardgameItemForm
    formset = RentBoardgameItemInlineFormSet
    extra = 0
    # fields = ['boardgame_number__boardgame', 'boardgame_number', 'quantity', 'rental_price', 'description']
    fieldsets = [
        ('Boardgame Number Details', {
            'fields': ['get_boardgame', 'boardgame_number', 'quantity', 'rental_price', 'description'],  # Hiển thị trường boardgame_number, description và boardgame_number.boardgame
        }),
        # Thêm các trường khác của RentBoardgameItem tùy ý ở đây
    ]
    readonly_fields = ['get_boardgame', 'boardgame_number', 'quantity', 'rental_price']

    def get_boardgame(self, obj):
        return obj.boardgame_number.boardgame if obj.boardgame_number else None
    get_boardgame.short_description = 'Boardgame' 

class RentBoardgameAdmin(admin.ModelAdmin):
    inlines = [RentBoardgameItemInline]
    list_display = ['renter', 'rid', 'start_date', 'end_date', 'order_status', 'rental_status', 'payment_status','deposit_refund_status', 'description']
    list_filter = ['renter', 'order_status', 'rental_status']

    def update_boardgame_numbers(self, obj):
        # print('update_boardgame_numbers')
        return obj.update_boardgame_numbers()

    def save_formset(self, request, form, formset, change):
        # print('save_formset')
        if isinstance(formset, RentBoardgameItemInlineFormSet):
            formset.save_m2m()
            for form in formset:
                if form.cleaned_data.get('description') and form.instance.boardgame_number:
                    form.instance.boardgame_number.description = form.cleaned_data['description']
                    form.instance.boardgame_number.save()
                    # print("---------------------------------------")
                    # print(f'form.instance.boardgame_number: {form.instance.boardgame_number}, {form.instance.boardgame_number.boardgame.in_stock}, {form.instance.boardgame_number.boardgame.order}, {form.instance.boardgame_number.boardgame.rental}')

        # Call the original save_formset method
        super().save_formset(request, form, formset, change)

    def save_related(self, request, form, formsets, change):
        # print('save_related')
        # print(f'form.instance: {form.instance}')
        # print("---------------------------------------")
        super().save_related(request, form, formsets, change)
        # Update the boardgame_number and boardgame attributes before saving related objects
        if form.instance:
            # boardgame, boardgame_number = self.update_boardgame_numbers(form.instance)
            self.update_boardgame_numbers(form.instance)

        # print("Updated Boardgame:", boardgame.in_stock, boardgame.order, boardgame.rental)
        # print("Updated BoardgameNumber:", boardgame_number)

    

class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'username', 'phone_number', 'email']
    list_filter = ['user_id', 'username']

# class GlobalSearchAdmin(admin.AdminSite):
#     def get_search_results(self, request, queryset, search_term):
#         search_fields = []
#         for model, model_admin in self._registry.items():
#             if hasattr(model_admin, 'search_fields'):
#                 search_fields.extend(model_admin.search_fields)
        
#         if search_fields:
#             q = Q()
#             for field in search_fields:
#                 q |= Q(**{field + '__icontains': search_term})
#             queryset = queryset.filter(q)
        
#         return queryset, False

# myadmin_site = GlobalSearchAdmin(name='myadmin')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Producer, ProducerAdmin)
admin.site.register(Boardgame, BoardgameAdmin)
admin.site.register(BoardgameReviews, BoardgameReviewsAdmin)
admin.site.register(RentBoardgame, RentBoardgameAdmin)
admin.site.register(User, UserAdmin)

# myadmin_site.register(Category, CategoryAdmin)
# myadmin_site.register(Version, VersionAdmin)
# myadmin_site.register(Author, AuthorAdmin)
# myadmin_site.register(Producer, ProducerAdmin)
# myadmin_site.register(Boardgame, BoardgameAdmin)
# myadmin_site.register(BoardgameReviews, BoardgameReviewsAdmin)
# myadmin_site.register(RentBoardgame, RentBoardgameAdmin)
# myadmin_site.register(User, UserAdmin)