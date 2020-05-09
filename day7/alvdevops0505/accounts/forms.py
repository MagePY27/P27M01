from django import forms
from django.contrib.auth import get_user_model

User = get_user_model() #相当于from users.models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(required=True, error_messages={'required': '用户名不能为空'})
    password = forms.CharField(required=True, error_messages={'required': '密码不能为空'})