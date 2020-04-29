from django.shortcuts import render,reverse
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from .models import students
from .form import StuModelForm

# Create your views here.
'''实现 使用form进行表单验证功能'''


class StuListView(TemplateView):
    template_name = 'stulist.html'
    model = students

    def get_context_data(self, **kwargs):
        context = super(StuListView,self).get_context_data(**kwargs)
        context["all_students"] = students.objects.all()
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
        print(context)
        return context

    def form_invalid(self, form_class):
        print(form_class)
        return self.render_to_response(self.get_context_data(form=form_class))


from django.contrib import messages
class StuUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'stuupdate.html'
    model = students
    #fields = "__all__"
    context_object_name = "stu"
    form_class = StuModelForm
    '''如果fields和form_class同时打开会报如下错误；因为fields走的是系统的model form验证，form_class走的是自定义的model form验证'''
    '''Specifying both 'fields' and 'form_class' is not permitted.'''
    success_message = "更新成功"
    #success_message = "%(name)s update successfully"

    def get_success_url(self):
        print('StuUpdateView request.POST是：',self.request.POST)
        print('StuUpdateView self.__dict__', self.__dict__)
        if '_continue' in self.request.POST:
            return reverse('students:update', kwargs={'pk': self.__dict__['kwargs']['pk']})
        return reverse('students:list')

    # def get_context_data(self, **kwargs):
    #     print('StuUpdateView get_context_data kwargs是：', kwargs)
    #     context = super(StuUpdateView, self).get_context_data()
    #     return context

    # def form_invalid(self, form_class):
    #     return self.render_to_response(self.get_context_data(form=form_class))

    def form_valid(self, form):
        messages.success(self.request, '更新成功')
        return super(StuUpdateView,self).form_valid(form)


class StuDeleteView(DeleteView):
    template_name = 'studelete.html'
    model = students
    context_object_name = "stu"

    def get_success_url(self):
        return reverse('students:list')
