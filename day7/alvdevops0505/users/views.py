from django.shortcuts import render, redirect, reverse
#from django.views.generic.base import View
from django.views.generic import View, DeleteView
#from django.urls import reverse

#Django自带的认证模块
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password

from .forms import UserModelForm, UserUpdateModelForm

from .models import UserProfile
# Create your views here.

# class IndexView(View):
#     def get(self, request):
#         if not request.user.is_authenticated:
#             return render(request, 'login.html', {})
#         return render(request, 'index.html', {})


# class IndexView(View):
#     #@method_decorator(login_required(login_url=reverse('accounts:login')))
#     @method_decorator(login_required(login_url='/accounts/login/'))
#     def get(self, request):
#         return render(request, 'index.html', {})

class IndexView(LoginRequiredMixin, View):
    # 当检测到用户没有登录时跳转的地址，默认可以在settings.py中设置 LOGIN_URL=XXX
    login_url = '/accounts/login/'
    #
    #redirect_field_name = 'reditect_to'
    redirect_field_name = None


    def get(self, request):
        return render(request, 'index.html', {})


class UserListView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = None
    def get(self, request):
        #all_users = UserProfile.objects.all()
        all_users = UserProfile.objects.exclude(username='admin')  #管理员admin不显示在列表页
        return render(request, 'userlist.html', {'all_users':all_users})


class UserAddView(LoginRequiredMixin, View):
    '''
    添加用户功能
    1、用户密码使用make_password模块加密后存储到数据库中
    2、使用modelform完成表单验证
    '''
    login_url = '/accounts/login/'
    redirect_field_name = None

    def get(self, request):
        #print(request.__dict__)
        #print(request.path_info)

        return render(request, 'userform.html', {'my_path':'add'})

    def post(self, request):
        #print(request.POST)
        UserFormData = UserModelForm(request.POST)
        #print(UserFormData)
        if UserFormData.is_valid():
            password = UserFormData.cleaned_data['password']
            #print(password)
            #print(make_password(password))
            #print(UserFormData.instance)  #如果我输入的用户名为zhoushuyu22 则UserFormData.instance就是zhoushuyu22
            UserFormData.instance.password = make_password(password)
            UserFormData.save()
            return redirect(reverse('users:list'))
        else:
            print(UserFormData.errors)
            return render(request, 'userform.html',{'UserFormData':UserFormData})


class UserUpdateView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = None

    def get(self, request, pk):
        ##print(request.__dict__)
        #print(request.path_info)
        #print(pk)
        user = UserProfile.objects.get(pk=pk)
        return render(request, 'userform.html',{'user':user, 'my_path':'update'})

    def post(self, request, pk):
        newdata = request.POST.dict()
        newdata.pop('csrfmiddlewaretoken')
        UserProfile.objects.filter(pk=pk).update(**newdata)
        return redirect(reverse('users:list'))



class UserDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    redirect_field_name = None

    template_name = 'userdel.html'
    model = UserProfile
    def get_success_url(self):
        return reverse('users:list')