from django import forms
from .models import RentBoardgame

class RentBoardgameForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'bg-gray-50 text-gray-900 text-sm rounded-lg self-center w-full pl-2 focus:outline-none', 'datepicker': True}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'bg-gray-50 text-gray-900 text-sm rounded-lg self-center w-full pl-2 focus:outline-none', 'datepicker': True}))

    class Meta:
        model = RentBoardgame
        fields = ['start_date', 'end_date']