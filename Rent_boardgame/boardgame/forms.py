from django import forms
# from stripe import Review
from boardgame.models import BoardgameReviews

class BoardgameReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': "Write review"
    }))

    class Meta:
        model = BoardgameReviews
        fields = ('review', 'rating')