from django import forms

class loginForm(forms.Form):
    username= forms.CharField(max_length=255,label="Email:")
    password=forms.CharField(label="Password:",widget=forms.PasswordInput)