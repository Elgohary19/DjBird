from django import forms
from .models import UserProfile



class UserRegisterForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    avatar = forms.ImageField()

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Password Must Match")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UserProfile.objects.filter(username__icontains=username).exists():
            raise forms.ValidationError("This user name is taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email__icontains=email).exists():
            raise forms.ValidationError("This e-mail is already registered")
        return email


