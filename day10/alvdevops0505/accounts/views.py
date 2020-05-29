from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .forms import LoginForm, ChangePasswordForm
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


'''
用户修改密码功能，对是否输入密码进行Form验证
对数据的密码1和确认密码是否一致的校验放在ChangePasswordView中
'''
class ChangePasswordView(View):
    def get(self, request):
        return render(request, 'change_password.html',{})

    def post(self, request):
        #print(request.POST) #<QueryDict: {'csrfmiddlewaretoken': ['kIk7B1mOtsixrXMimraD9skBh2CrHeouaRxEbqxgAGgycjFMoQnDNRGgoBfVa5bg'], 'old_password': ['1'], 'password': ['2'], 'password2': ['3']}>
        ChangePasswordFormDate = ChangePasswordForm(request.POST)
        id = request.user.id
        if ChangePasswordFormDate.is_valid():
            password1 = ChangePasswordFormDate.cleaned_data['password1']
            password2 = ChangePasswordFormDate.cleaned_data['password2']
            if password1 == password2:
                hasher_pass = make_password(password2)
                user = User.objects.get(id=id)
                user.password = hasher_pass
                user.save()
                return HttpResponseRedirect(reverse('account:login'))
            else:
                errmsg = "两次密码不一致"
                return render(request, 'change_password.html', {'errmsg': errmsg})
        else:
            print(ChangePasswordFormDate.errors)
            return render(request, 'change_password.html', {'form':ChangePasswordFormDate})

#2020-05-16
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from .forms import PasswordChangeForm
from django.urls import reverse_lazy

class PasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    """
    更新密码（登录状态下，个人修改自己的密码）
    https://docs.djangoproject.com/zh-hans/2.2/topics/auth/customizing/
    https://it.ismy.fun/2019/08/09/django-change-password-views/  密码修改后不会自动退出
    """
    template_name = 'change_password.html'
    model = User
    form_class = PasswordChangeForm
    success_url = reverse_lazy('accounts:password_change_done')

    # 因为要检查当前登录用户的密码对不对，故而将当前登录用户传到表单类中
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)

class PasswordChangeDoneView(TemplateView):
    template_name = 'change_password_done.html'