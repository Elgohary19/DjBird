from django import forms
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from . import models


User = get_user_model()

class UserRegisterForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)


    def clean_password2(self):
        password = self.cleaned_data('password')
        password2 = self.cleaned_data('password2')
        if password != password2:
            raise forms.ValidationError("Password Must Match")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__icontains=username).exists():
            raise forms.ValidationError("This user name is taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__icontains=email).exists():
            raise forms.ValidationError("This e-mail is already registered")
        return email


class UserDataForm(forms.ModelForm):
    class Meta:
        model = models.UserData
        fields = ['image', 'country']
