from django import forms
from .models import User

class MyForm(forms.ModelForm):
    bsform="form-control p-2 mb-3 "
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username','class':bsform}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'email','class':bsform}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password','class':bsform}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password',]