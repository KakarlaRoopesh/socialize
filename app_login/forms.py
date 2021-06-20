from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile




class CreateNewUser(UserCreationForm):
    email = forms.EmailField(required=True,label='',widget=forms.TextInput(attrs={'placeholder':'EMAIL'}))
    username = forms.CharField(required=True,label='',widget=forms.TextInput(attrs={'placeholder':'USERNAME'}))
    password1 = forms.CharField(required=True,label='',widget=forms.PasswordInput(attrs={'placeholder':'PASSWORD'}))
    password2 = forms.CharField(required=True,label='',widget=forms.PasswordInput(attrs={'placeholder':'PASSWORD CONFIRMATION'}))

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'password1',
            'password2'
        )


class EditProfile(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)



