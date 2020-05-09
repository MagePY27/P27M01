from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .forms import LoginForm
# Create your views here.

User = get_user_model() #

class LoginView(View):
    def get(self, request):
        login_form = LoginForm() #在这里做表单验证有什么用？
        return render(request,'login.html',{'login_form': login_form})

    def post(self, request):
        form = LoginForm(request.POST)
        '''
        表单验证，比如用户名输入的是a,密码输入的是1，则form的输出结果的
        <tr><th><label for="id_username">Username:</label></th><td><input type="text" name="username" value="a" required id="id_username"></td></tr>
        <tr><th><label for="id_password">Password:</label></th><td><input type="text" name="password" value="1" required id="id_password"></td></tr>
        '''
        if form.is_valid():
            '''
            form.cleaned_data 是一个字典 {'username': 'a', 'password': '1'}
            '''
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    #print(request.__dict__)
                    #print(request.user) #request.user 输出登陆用户admin
                    #return HttpResponse('登陆成功')
                    return HttpResponseRedirect(reverse('users:index')) #跳转到index页面
                else:
                    return render(request, 'login.html', {'form': form, 'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'form': form, 'msg': '用户名或密码错误或用户不存在'})
        else:
            return render(request, 'login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("accounts:login"))