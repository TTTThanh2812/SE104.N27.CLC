from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from boardgame.models import BoardgameNumbers
from rent.models import RentBoardgameItem

class RentBoardgameForm(forms.Form):
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}))
    quantity = forms.IntegerField(label='Quantity', min_value=1)

    def __init__(self, *args, **kwargs):
        self.boardgame_number = kwargs.pop('boardgame_number', None)
        super().__init__(*args, **kwargs)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']

        if self.boardgame_number:
            # Get the boardgame number object
            boardgame_number = BoardgameNumbers.objects.filter(boardgame=self.boardgame_number).first()
            if not boardgame_number:
                raise ValidationError(_('Invalid boardgame number.'))
            if quantity > boardgame_number.in_stock:
                raise ValidationError(_('Not enough boardgame numbers in stock.'))

        return quantity

class RentBoardgameItemForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, required=False)
    # boardgame_number_status = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = RentBoardgameItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Fetch the related BoardgameNumbers instance if it exists
        # try:
        #     boardgame_number = self.instance.boardgame_number
        #     if boardgame_number:
        #         # Set initial value for the description field
        #         self.initial['description'] = boardgame_number.description
        # except RentBoardgameItem.boardgame_number.RelatedObjectDoesNotExist:
        #     pass
    def clean(self):
        cleaned_data = super().clean()

        # Lấy giá trị description từ form và boardgame_number từ instance
        description = cleaned_data.get('description')
        boardgame_number = self.instance.boardgame_number

        # Kiểm tra nếu description và boardgame_number tồn tại
        if description and boardgame_number:
            # Cập nhật mô tả trong boardgame_number và lưu vào database
            boardgame_number.description = description
            boardgame_number.save()

        return cleaned_data

    def save_m2m(self):
        """
        This method is called to save the ManyToMany fields related to the form.
        """
        # Perform any additional operations related to ManyToMany fields if needed
        pass