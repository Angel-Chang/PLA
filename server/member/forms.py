from django import forms
from django.contrib import messages

class LoginForm(forms.Form):
    user_id  = forms.CharField(label="帳號",max_length=20)
    user_pwd = forms.CharField(label="密碼",widget=forms.PasswordInput())