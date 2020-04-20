from django import forms
from students.models import students

import re

class StuModelForm(forms.ModelForm):
    confirm_password = forms.CharField(required=True)

    class Meta:
        model = students
        fields = "__all__"

    #在modelForm校验的基础上，比如name字段最长是10个字符；现在在添加一个校验规则：name字段如果过小，比如小于3个字符，也不能通过校验
    def clean_name(self):
        cname = self.cleaned_data['name']
        if len(cname) < 3:
            print('cname是：', cname)
            raise forms.ValidationError('用户名长度小于3')
        else:
            return cname
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
        print("32:", self.cleaned_data) #输出结果 32: {'name': 'zhoushuyu', 'phone': '15690751671', 'sex': 0, 'password': 'sda', 'confirm_password': 'dasf'}
        confirm_password = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        if confirm_password != password:
            raise forms.ValidationError('两次密码不一致')

        return confirm_password