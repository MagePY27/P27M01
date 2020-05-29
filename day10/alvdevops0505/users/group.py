# from django.views.generic import ListView
#
# from django.contrib.auth.models import Permission
# from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# from django.db.models import Q

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Group, Permission

from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.views.generic.base import View, TemplateView

from pure_pagination.mixins import PaginationMixin

from django.contrib.auth import get_user_model

User = get_user_model()



# class PermListView(LoginRequiredMixin, ListView):
#     login_url = '/accounts/login/'
#     redirect_field_name = None
#
#     template_name = 'permission_list.html'
#     model = Permission

class PermListView(LoginRequiredMixin, PermissionRequiredMixin, PaginationMixin,  ListView):
    """
    权限列表
    """
    template_name = 'permission_list.html'
    model = Permission
    paginate_by = 10
    permission_required = 'auth.view_permission'
    keyword = None

    def get_query_term(self):
        self.keyword = self.request.GET.get('keyword', None)
        return self.keyword

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(content_type__model__in=['logentry', 'session', 'contenttype'])
        keyword = self.get_query_term()
        if keyword:
            queryset = queryset.filter(Q(name__icontains=keyword) | Q(content_type__app_label__icontains=keyword) |
                                       Q(codename__icontains=keyword))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context


class PermAddView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """
    添加权限
    """
    template_name = 'permission_add.html'
    model = Permission
    fields = ('name', 'content_type', 'codename')
    success_message = '%(name)s 权限添加成功！'
    permission_required = 'auth.add_permission'

    def get_success_url(self):
        if '_addanother' in self.request.POST:
            return reverse('users:perm_add')
        return reverse('users:perm_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_types = ContentType.objects.all()
        context['content_types'] = content_types
        return context
#
#
class PermUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    更新权限
    """
    template_name = 'permission_update.html'
    model = Permission
    fields = ('name',)
    success_message = '%(name)s 权限更新成功！'
    permission_required = 'auth.change_permission'

    def get_success_url(self):
        if '_addanother' in self.request.POST:
            return reverse('users:perm_add')
        elif '_savedit' in self.request.POST:
            return reverse('users:perm_update', kwargs={'pk': self.object.pk})
        return reverse('users:perm_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_types = ContentType.objects.all()
        context['content_types'] = content_types
        return context
#
#
# class PermDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
#     """
#     删除权限
#     """
#     template_name = 'permission_delete.html'
#     model = Permission
#     permission_required = 'auth.delete_permission'
#
#     def delete(self, request, *args, **kwargs):
#         response = super().delete(request, *args, **kwargs)
#         #messages.success(request, '{} 组删除成功~'.format(self.object.name))
#         return response
#
#     def get_success_url(self):
#         return reverse_lazy('users:perm_list')


# class GroupListView(View):
#     def get(self, request):
#         all_groups = Group.objects.all()
#         return render(request, 'group_list1.html', {'all_groups': all_groups})
class GroupListView(LoginRequiredMixin, PermissionRequiredMixin, PaginationMixin, ListView):

# class GroupListView(LoginRequiredMixin, PaginationMixin, ListView):
    """
    组列表
    """
    template_name = 'group_list.html'
    model = Group
    ordering = 'id'
    paginate_by = 10
    permission_required = 'auth.view_group'
    keyword = ""

    def get_keyword(self):
        self.keyword = self.request.GET.get('keyword')
        return self.keyword

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.get_keyword()
        if keyword:
            queryset = queryset.filter(name__icontains=keyword)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context


class GroupAddView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """
    添加组
    """
    template_name = 'group_add.html'
    model = Group
    fields = ('name', 'permissions')
    success_message = '%(name)s 组添加成功！'
    permission_required = 'auth.add_group'

    def get_success_url(self):
        if '_addanother' in self.request.POST:
            return reverse('users:group_add')
        return reverse('users:group_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        permissions = Permission.objects.exclude(Q(content_type__model='session') |
                                                 Q(content_type__model='contenttype') |
                                                 Q(content_type__model='logentry') |
                                                 Q(codename='add_permission') |
                                                 Q(codename='delete_permission')
                                                 ).values('id', 'name',
                                                          'content_type__app_label',
                                                          'codename')
        context['permissions'] = permissions
        return context


class GroupUpdateView(UpdateView):
    template_name = 'group_update.html'
    model = Group
    fields = '__all__'

    def get_success_url(self):
        if '_addanother' in self.request.POST:
            return reverse('users:group_add')
        elif '_savedit' in self.request.POST:
            return reverse('users:group_update', kwargs={'pk': self.kwargs['pk']})
        else:
            return reverse('users:group_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #permissions = Permission.objects.all()
        permissions = Permission.objects.exclude(Q(content_type__model='session')|Q(content_type__model='contenttype')
                                                 |Q(content_type__model='logentry'))
        context['permissions'] = permissions
        return context


class GroupDeleteView(DeleteView):
    template_name = 'group_confirm_delete.html'
    model = Group

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, '{} 组删除成功~'.format(self.object.name))
        return response
    def get_success_url(self):
        return reverse_lazy('users:group_list')

class AddUserToGroupView(View):
    def get(self, request, pk):
        #group = Group.objects.get()
        group = get_object_or_404(Group,pk=pk)
        users = User.objects.all()
        context = {'group':group, 'users':users}
        return render(request, 'group_add_user.html', {'context': context, 'users':users, 'group':group})

    def post(self, request, pk):
        uids = request.POST.getlist('users')
        print(uids)
        group = get_object_or_404(Group,pk=pk)
        if uids:
            users = User.objects.filter(id__in=uids)
            print(users)
            group.user_set.set(users)
        else:
            group.user_set.clear()
        messages.success(request,'{}组添加用户成功或移除用户成功'.format(group))
        return HttpResponseRedirect(reverse('users:group_list'))