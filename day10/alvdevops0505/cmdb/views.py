''''
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView
from django.views.generic.base import View
from pure_pagination import PaginationMixin

# Create your views here.
from cmdb.models import Host,DataBase, Tag, Type

from .tasks import  update_hosts_from_cloud, file, useradd
'''

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required, permission_required

from pure_pagination import PaginationMixin
#from pure_pagination.mixins import PaginationMixin

from cmdb.models import Tag, Type, Host, DataBase

#from .tasks1 import file, update_hosts_from_cloud
from .tasks import  update_hosts_from_cloud, file, useradd

class IndexView(View):
    def get(self, request):
        # 存钱
        file.delay()
        return HttpResponse("ok")


#class TypeListView(LoginRequiredMixin, PermissionRequiredMixin, PaginationMixin, ListView):
class TypeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    标签类型列表
    """
    model = Type
    paginate_by = 10
    permission_required = 'cmdb.view_type'
    keyword = None


    def get_keyword(self):
        self.keyword = self.request.GET.get('keyword')
        return self.keyword

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.get_keyword()
        if keyword:
            queryset = queryset.filter(Q(name__icontains=keyword) | Q(name_cn__icontains=keyword))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['keyword'] = self.keyword
        return context

class TypeAddView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """
    创建标签类型
    """
    model = Type
    fields = ('name', 'name_cn')
    permission_required = 'cmdb.add_type'
    success_message = '添加 %(name)s 类型成功'

    def get_success_url(self):
        if '_addanother' in self.request.POST:
            return reverse('cmdb:type-add')
        return reverse('cmdb:types')


class TypeEditView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    编辑标签
    """
    model = Type
    fields = ('name', 'name_cn')
    permission_required = 'cmdb.change_type'
    success_message = '标签类型 %(name_cn)s 编辑成功！'

    def get_success_url(self):
        if '_addanother' in self.request.POST:
            return reverse('cmdb:type-add')
        elif '_savedit' in self.request.POST:
            return reverse('cmdb:type-edit', kwargs={'pk': self.object.pk})
        else:
            return reverse('cmdb:types')


class TypeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    删除类型
    """
    model = Type
    permission_required = 'cmdb.delete_type'

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, '{} 标签类型删除成功！'.format(self.object.name_cn))
        return response

    def get_success_url(self):
        return reverse_lazy('cmdb:types')

#class TagListView(LoginRequiredMixin, PermissionRequiredMixin, PaginationMixin, ListView):
class TagListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    标签列表
    """
    model = Tag
    paginate_by = 10
    permission_required = 'cmdb.view_tag'
    keyword = None

    def get_keyword(self):
        self.keyword = self.request.GET.get('keyword')
        return self.keyword

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.get_keyword()
        if keyword:
            queryset = queryset.filter(Q(name__icontains=keyword) | Q(name_cn__icontains=keyword) |
                                       Q(type__name__icontains=keyword) | Q(type__name_cn__icontains=keyword))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['keyword'] = self.keyword
        return context


class TagAddView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """
    创建标签
    """
    model = Tag
    fields = ('type', 'name', 'name_cn')
    permission_required = 'cmdb.add_tag'
    success_message = '添加 %(name_cn)s 标签成功~'

    def get_success_url(self):
        if '_addanother' in self.request.POST:
            return reverse('cmdb:tag-add')
        return reverse('cmdb:tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = Type.objects.all()
        return context


class TagEditView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    编辑标签
    """
    model = Tag
    fields = ('type', 'name', 'name_cn')
    permission_required = 'cmdb.change_tag'
    success_message = '%(name_cn)s 标签编辑成功！'

    def get_success_url(self):
        if '_addanother' in self.request.POST:
            return reverse('cmdb:tag-add')
        elif '_savedit' in self.request.POST:
            return reverse('cmdb:tag-edit', kwargs={'pk': self.object.pk})
        return reverse('cmdb:tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = Type.objects.all()
        return context


class TagDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    删除标签
    """
    model = Tag
    permission_required = 'cmdb.delete_tag'

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, '{} 标签删除成功！'.format(self.object.name_cn))
        return response

    def get_success_url(self):
        return reverse_lazy('cmdb:tags')


class HostListView(LoginRequiredMixin, PermissionRequiredMixin, PaginationMixin, ListView):
    """
    主机列表
    """
    model = Host
    paginate_by = 10
    permission_required = 'cmdb.view_host'
    keyword = None
    slug = None

    def get_keyword(self):
        self.keyword = self.request.GET.get('keyword')
        return self.keyword
    #得到前端传来的标签
    def get_slug(self):
        self.slug = self.request.GET.get('tag')
        return self.slug

    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.get_slug()
        if slug:
            queryset = queryset.filter(tags__name=slug)
        keyword = self.get_keyword()
        if keyword:
            queryset = queryset.filter(Q(instance_id__icontains=keyword) | Q(instance_name__icontains=keyword) |
                                       Q(description__icontains=keyword) | Q(hostname__icontains=keyword) |
                                       Q(public_ip__icontains=keyword) | Q(private_ip__icontains=keyword))
        return queryset
    #重写get_context_data将变量和对应的数据传递到前端
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['keyword'] = self.keyword
        context['slug'] = self.slug
        context['types'] = Type.objects.all()
        context['tags'] = Tag.objects.all()
        context['hosts_count'] = Host.objects.count()
        return context


class HostTagAddView(LoginRequiredMixin, UpdateView):
    """
    给主机添加标签
    """
    template_name = 'cmdb/host_tags.html'
    model = Host
    fields = ('tags',)

    def get_success_url(self):
        if '_addanother' in self.request.POST:
            return reverse('cmdb:host-tags-add', kwargs={'pk': self.object.pk})
        return reverse('cmdb:hosts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['hosts_tags'] = self.object.tags.all()
        return context


class HostAddByTagView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    通过标签添加主机或更新
    """
    permission_required = 'cmdb.change_tag'

    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        hosts = Host.objects.all()
        selected_hosts = tag.host_set.all()
        context = {'hosts': hosts, 'selected_hosts': selected_hosts, 'tag': tag}
        return render(request, 'cmdb/host_add_by_tag.html', context=context)

    def post(self, request, pk):
        host_ids = request.POST.getlist('hosts')
        tag = get_object_or_404(Tag, pk=pk)
        if host_ids:
            hosts = Host.objects.filter(id__in=host_ids)
            tag.host_set.set(hosts)
        else:
            tag.host_set.clear()
        if '_savedit' in request.POST:
            return HttpResponseRedirect(reverse('cmdb:add-hosts', kwargs={'pk': pk}))
        return HttpResponseRedirect(reverse('cmdb:tags'))


@require_GET
@login_required
def update_host_info(request):
    """
    更新主机信息
    :param request:
    :return:
    """
    update_hosts_from_cloud.delay()
    return HttpResponse('任务已提交到后台，请稍等片刻！')

from django.db.models import Count
from django.db import connection
class AssetsOverView(LoginRequiredMixin, View):
    """
    资产大盘
    """
    def get(self, request):
        overview = {}

        '''1、多云资产分布统计'''
        #[{"name": "阿里云", "value": 40}, {"name": "腾讯云", "value": 26}]
        HostGroupBy = Host.objects.values('public_cloud').annotate(Count('public_cloud'))
        DBGroupBy = DataBase.objects.values('public_cloud').annotate(Count('public_cloud'))
        HostGroupByList=[]
        for i in HostGroupBy:
            for j in DBGroupBy:
                if i.get('public_cloud') == j.get('public_cloud'):
                    counts = i.get('public_cloud__count') + j.get('public_cloud__count')
                    HostGroupByList.append({"name":i.get('public_cloud'), "value": counts})
            #HostGroupByList.append({"name":i.get('public_cloud'),"value":i.get('public_cloud__count')})
        overview['clouds_asset_count']=HostGroupByList

        '''2、不同类型资产占比'''
        HostAll = Host.objects.count()
        DataBaseAll = DataBase.objects.count()
        overview['each_type_assets_count'] = [{'name': '服务器','value':HostAll},{'name':'数据库','value':DataBaseAll}]
        #[{'name': '服务器', 'value': 54}, {'name': 'RDS', 'value': 5}, {'name': 'NAS', 'value': 7}]


        '''3、业务线资产占比，这个不会用ORM写，自己实现的感觉太复杂'''
        #[{'name': '未分配', 'value': 41}, {'name': '商城', 'value': 3}]
        #overview.business_line_host_nums
        BusinessLineHostByList = []
        cursor=connection.cursor()
        cursor.execute("select a.name_cn, count(a.name_cn) from cmdb_tag a,cmdb_host_tags b, cmdb_host c where b.tag_id = a.id and b.host_id = c.id GROUP BY(a.name_cn)")
        CursorAll = cursor.fetchall()
        print(CursorAll)  #(('拓扑管理服务器', 1), ('身份管理服务器', 2))
        #得到所有的HOST服务器，进行统计
        YHost_Count = Host.objects.all().count()
        #得到没有分配标签的服务器数量
        TagHostNum = 0
        for x in CursorAll:
            TagHostNum = TagHostNum + x[1]
            BusinessLineHostByList.append({'name': x[0],'value': x[1]})
        UnTagHostNum = YHost_Count - TagHostNum
        BusinessLineHostByList.append({'name':'未分配','value':UnTagHostNum})
        overview['business_line_host_nums'] = BusinessLineHostByList


        '''标签云'''
        #var word_list = [{'text': '数据库', 'weight': 2, 'link': '/assets/hosts/?tag=db'}]
        TagCloudList = []
        AllTags = Tag.objects.all()
        for i in AllTags:
            if i.host_set.all():
                TagCloudList.append({'text':i.name, 'weight':i.host_set.all().count(),'link':'/cmdb/hosts/?tag='+i.name})
                #print('标签云',i.name,i.host_set.all().count())
        # print(TagCloudList)
        overview['tag_cloud'] = TagCloudList
        # print(overview)
        context = {
            'overview': overview,
        }
        return render(request, 'cmdb/assets_overview.html', context=context)