from django import forms
from users.models import UserProfile

import re


class UserModelForm(forms.ModelForm):
    confirm_password = forms.CharField(required=True)

    class Meta:
        model = UserProfile
        fields = ['username','password','phone','sex']

    #通过正则表达式验证手机号是否合法
    def clean_phone(self):
        cphone = self.cleaned_data['phone']
        phone_regex = r'^1[345678][0-9]{9}$'
        p = re.compile(phone_regex)
        if p.match(cphone):
            return cphone
        else:
            raise forms.ValidationError('手机号不合法')

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        if confirm_password != password:
            raise forms.ValidationError('两次密码不一致')

        return confirm_password

class UserUpdateModelForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'phone', 'sex']

    # 通过正则表达式验证手机号是否合法
    def clean_phone(self):
        cphone = self.cleaned_data['phone']
        phone_regex = r'^1[345678][0-9]{9}$'
        p = re.compile(phone_regex)
        if p.match(cphone):
            return cphone
        else:
            raise forms.ValidationError('手机号不合法')


# from django import forms
# from django.contrib.auth import  get_user_model
#
from django.contrib.auth import get_user_model
User = get_user_model()


class ResetPasswordForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('password',)

    # def __init__(self, *args, **kwargs):
    #     super(ResetPasswordForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('输入的两次密码不一致，请重新输入！')
        return password2