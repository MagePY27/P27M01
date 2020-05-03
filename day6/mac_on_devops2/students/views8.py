from django.views.generic import View, ListView, TemplateView, DetailView
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, QueryDict
from django.urls import reverse

from .models import students
from .form import StuModelForm


class AddStu(TemplateView):
    template_name = 'stuadd_jq.html'


class ListStu(ListView):
    template_name = 'stulist_jq.html'
    model = students
    context_object_name = "all_students"
    '''通过上面3行，就可以将数据从数据库中全部拿到，然后渲染到stulist_jq.html中'''

    def post(self, request):
        print(request.POST)
        StuFormdata = StuModelForm(request.POST)
        if StuFormdata.is_valid():
            StuFormdata.save() #将通过表单验证的数据保存到数据库中
            res = {'code':0, 'msg':'用户添加成功', 'next_url':reverse('students:jlist')}
        else:
            #print(StuFormdata.errors.as_json())
            print(StuFormdata.errors.as_text())
            res = {'code':1, 'errmsg':StuFormdata.errors.as_text(), 'next_url':reverse('students:jadd')}
        #return render(request, 'stulist.html')
        return JsonResponse(res)

    '''删除用户'''
    def delete(self, request):
        data = QueryDict(request.body).dict() #通过前端ajax将ID传递到后端
        print(data)
        pk = data.get('id')
        try:
            user = self.model.objects.filter(pk=pk)
            user.delete()
            res = {'code':0, 'result':'删除用户成功'}
        except:
            res = {'code':1, 'errmsg':'删除用户失败'}
        return JsonResponse(res, safe=True)


class DetailStu(DetailView):
    template_name = 'stuupdate_jq.html'
    model = students
    context_object_name = "stu"

    def get_object(self, queryset=None):
        obj = super(DetailStu, self).get_object()
        return obj

    def post(self, request, **kwargs):
        print(request.POST)
        print(kwargs) #例子 {'pk': '3'}
        user = students.objects.get(pk=kwargs['pk'])
        StuFormdata = StuModelForm(request.POST, instance=user)  #modelform对象instance是什么作用？
        if StuFormdata.is_valid():
            try:
                print(StuFormdata)
                StuFormdata.save()#将数据保存到数据库
                res = {'code':0, 'result': '用户更新成功', 'next_url':reverse('students:jlist')}
            except:
                res = {'code':1, 'errmsg': '用户更新失败', 'next_url':reverse('students:jlist')}
        else:
            print(StuFormdata.errors)
            res = {'code': 1, 'errmsg': StuFormdata.errors, 'next_url': reverse('students:jlist')}
        return render(request,'jump_jq.html',res)


# class AddStu(View):
#     def get(self, request):
#         return render(request, 'stuadd_jq.html')
#
#     def post(self, request):
#         print(request.POST)
#         return render(request, 'stuadd_jq.html')



