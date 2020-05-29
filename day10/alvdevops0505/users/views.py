from django.shortcuts import render, redirect, reverse, HttpResponse
#from django.views.generic.base import View
from django.views.generic import View, DeleteView, UpdateView, ListView
from django.http import HttpResponseRedirect
#from django.urls import reverse

#Django自带的认证模块
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission
from django.contrib.messages.views import SuccessMessageMixin

from .forms import UserModelForm, UserUpdateModelForm

from .models import UserProfile
from django.db.models import Q

from django.contrib.auth import get_user_model

User = get_user_model()
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



#0519 +
from pure_pagination.mixins import PaginationMixin
class UserListView(LoginRequiredMixin, PermissionRequiredMixin, PaginationMixin,ListView):
    """
    用户列表
    """
    template_name = "list.html"
    model = User
    permission_required = 'users.view_userprofile'
    paginate_by = 10
    keyword = ""

    # 数据过滤
    def get_queryset(self):
        queryset = super(UserListView, self).get_queryset()
        queryset = queryset.exclude(username='admin')
        self.keyword = self.request.GET.get("keyword", "")
        if self.keyword:
            queryset = queryset.filter(Q(name__icontains=self.keyword) |
                                       Q(username__icontains=self.keyword) |
                                       Q(phone__icontains=self.keyword))

        return queryset

    # 搜索关键字传给前端
    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context

#class UserListView(LoginRequiredMixin, View):
#
#     login_url = '/accounts/login/'
#     redirect_field_name = None
#     def get(self, request):
#         #all_users = UserProfile.objects.all()
#         all_users = UserProfile.objects.exclude(username='admin')  #管理员admin不显示在列表页
#         return render(request, 'userlist.html', {'all_users':all_users})


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


#为用户添加组（角色）
class UserGroupView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'user_newgrp.html'
    model = User
    fields = ('groups',)
    success_message = '加入或退出组成功'
    permission_required = 'users.change_user'
    context_object_name = 'username'

    def get_success_url(self):
        print(self.__dict__)
        return reverse('users:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        groups = Group.objects.all()
        context['groups'] = groups
        print(context)
        return context
''' 自己写的
class UserGroupView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'auth.change_group'

    def get(self, request, pk):
        user = UserProfile.objects.get(pk=pk)
        groups_on_user = user.groups.all()
        print(groups_on_user)
        all_groups = Group.objects.all()
        print(all_groups)
        # return HttpResponse('OK')

        return render(request, 'user_group.html',{'groups_on_user': groups_on_user, 'all_groups': all_groups})

    def post(self, request, pk):
        # <QueryDict: {'group_name': ['1', '3', '1'], '_save': [''], 'csrfmiddlewaretoken': ['x7wJ2nUPduqsiWYwKxHu6ClWS9bpikqlOiwrJsgOsVN6UOt3oH7pbeK45DEIilgl']}>
        # querydict对象中group_name是一个列表，使用getlist方法得到这个列表,使用set去重，然后再转换为list
        print(request.POST)
        groups = list(set(request.POST.getlist('group_name')))
        #print(groups)
        user = UserProfile.objects.get(pk=pk)
        # print(user, groups)
        user.groups.set(groups)
        #return reverse('users:list')
        #return render(request, 'userlist.html')
        return HttpResponseRedirect(reverse('users:list'))
'''

#2020-05-16 T +
class UserPermissionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    更新用户权限
    """
    template_name = 'user_permission_update.html'
    model = User
    fields = ('user_permissions',)
    success_message = '用户权限编辑成功！'
    permission_required = 'users.change_user'
    context_object_name = 'username'

    def get_success_url(self):
        if '_addanother' in self.request.POST:
            return reverse('users:user-perm-update', kwargs={'pk': self.kwargs.get('pk')})
        return reverse('users:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        permissions = Permission.objects.exclude(Q(content_type__model='session') |
                                                 Q(content_type__model='contenttype') |
                                                 Q(content_type__model='logentry')
                                                 ).values('id', 'name',
                                                          'content_type__model', 'content_type__app_label',
                                                          'codename')
        context['permissions'] = permissions
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(UserPermissionUpdateView, self).form_valid(form)


from users.forms import ResetPasswordForm
class ResetPasswordView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    管理员重置密码
    """
    template_name = 'reset_password.html'
    model = User
    form_class = ResetPasswordForm
    # fields = ('password',)
    permission_required = 'auth.change_user'
    success_message = '重置密码成功！'

    def get_success_url(self):
        return reverse('users:list')

    def form_valid(self, form):
        password = form.cleaned_data.get('password')
        print(password)
        # password = make_password(password) #make_password函数与下面的set_password函数功能上是一样的
        # user.password = password
        # user.save()
        self.object.set_password(password)
        self.object.save()
        return super(ResetPasswordView, self).form_valid(form)