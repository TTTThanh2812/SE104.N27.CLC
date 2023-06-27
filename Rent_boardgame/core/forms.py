from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from userauths.models import User

class PasswordChangeCustomForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput,
    )

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        user = self.user
        if not user.check_password(old_password):
            raise forms.ValidationError("Incorrect old password.")
        return old_password
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'phone_number', 'address']