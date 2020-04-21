from django.shortcuts import render,reverse, HttpResponse
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin

from .models import students
from .form import StuModelForm

# Create your views here.
'''实现 使用form进行表单验证功能'''


class StuListView(ListView):
    template_name = 'stulist.html'
    model = students
    context_object_name = "all_students"

    '''实现搜索功能'''
    def get_queryset(self):
        queryset = super(StuListView, self).get_queryset()
        print(queryset)
        self.keyword = self.request.GET.get('keyword','')
        if self.keyword:
            queryset = queryset.filter(name__icontains = self.keyword)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(StuListView,self).get_context_data(**kwargs)
        context["keyword"] = self.keyword
        return context


class StuAddView(CreateView):
    template_name = 'stuadd.html'
    model = students
    #自己写modelForm进行表单验证
    form_class = StuModelForm

    #fields = ('name','phone','sex','password')

    def get_success_url(self):
        return reverse('students:list')

    def get_context_data(self, **kwargs):
        context = super(StuAddView, self).get_context_data()
        print("35行context是: ",context)
        return context

    def form_invalid(self, form_class):
        print("39行form_class是: ",form_class)
        return self.render_to_response(self.get_context_data(form=form_class))

'''
class StuUpdateView(DetailView):
    template_name = 'stuedit.html'
    model = students
    context_object_name = "stu"

    def post(self, request, **kwargs):
        #print(self.request)
        #print(self.kwargs) # 得到pk=1
        pk = kwargs['pk']
        student = students.objects.get(pk=pk)
        studentForm = StuModelForm(request.POST, instance=student)
        #print(studentForm)
        if studentForm.is_valid():
            print(studentForm.cleaned_data)
            studentForm.save()
            msg = {'code':0, 'result':'更新成功'}
        else:
            print(studentForm.errors)
            msg = {'code':1, 'err':'表单验证失败'}
        return render(request, 'jump_page.html', {'msg':msg, 'studentForm':studentForm})
'''


class StuUpdateView(UpdateView):
    template_name = 'stuupdate.html'
    model = students
    #fields = "__all__"
    context_object_name = "stu"
    form_class = StuModelForm
    #如果fields和form_class同时打开会报如下错误；因为fields走的是系统的model form验证，form_class走的是自定义的model form验证
    #Specifying both 'fields' and 'form_class' is not permitted.


    def get_success_url(self):
        print('StuUpdateView request.POST是：',self.request.POST)
        print('StuUpdateView self.__dict__', self.__dict__)
        if '_continue' in self.request.POST:
            return reverse('students:update', kwargs={'pk': self.__dict__['kwargs']['pk']})
        return reverse('students:list')

    def get_context_data(self, **kwargs):
        print('StuUpdateView get_context_data kwargs是：', kwargs)
        context = super(StuUpdateView, self).get_context_data()
        return context

    def form_invalid(self, form_class):
        print('form_class', form_class)
        return self.render_to_response(self.get_context_data(form=form_class))

# def form_valid(self, form):
#     #     messages.success(self.request, '更新成功')
#     #     return super(StuUpdateView,self).form_valid(form)


class StuDeleteView(DeleteView):
    template_name = 'studelete.html'
    model = students
    context_object_name = "stu"

    def get_success_url(self):
        return reverse('students:list')
