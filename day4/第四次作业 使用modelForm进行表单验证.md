<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/><meta name="exporter-version" content="Evernote Mac 9.3.3 (459822)"/><meta name="author" content="zhoushuyu215@163.com"/><meta name="created" content="2020-04-20 15:08:40 +0000"/><meta name="source" content="desktop.mac"/><meta name="updated" content="2020-04-20 15:22:05 +0000"/><meta name="content-class" content="yinxiang.markdown"/><title>第四次作业 使用modelForm进行表单验证</title></head><body><div style="font-size: 14px; margin: 0; padding: 0; width: 100%;"><h3 style="line-height: 160%; box-sizing: content-box; font-weight: 700; font-size: 27px; color: #333;">用户展示功能</h3>
<pre style="line-height: 160%; box-sizing: content-box; border: 0; border-radius: 0; margin: 2px 0 8px; background-color: #f5f7f8;"><code style="display: block; overflow-x: auto; background: #1e1e1e; line-height: 160%; box-sizing: content-box; border: 0; border-radius: 0; letter-spacing: -.3px; padding: 18px; color: #f4f4f4; white-space: pre-wrap;">class StuListView(TemplateView):
    template_name = 'stulist.html'
    model = students

    def get_context_data(self, **kwargs):
        context = super(StuListView,self).get_context_data(**kwargs)
        context["all_students"] = students.objects.all()
        return context
</code></pre>
<p style="line-height: 160%; box-sizing: content-box; margin: 10px 0; color: #333;">访问URL<br/>
http://127.0.0.1:9000/students/list/<br/>
效果图<br/>
<img src="%E7%AC%AC%E5%9B%9B%E6%AC%A1%E4%BD%9C%E4%B8%9A%20%E4%BD%BF%E7%94%A8modelForm%E8%BF%9B%E8%A1%8C%E8%A1%A8%E5%8D%95%E9%AA%8C%E8%AF%81.resources/A22C7BD8-1EA0-4D72-93CD-F2E47A23A8FB.png" height="962" width="1164"/></p>
<p style="line-height: 160%; box-sizing: content-box; margin: 10px 0; color: #333;">缺陷：目前未实现搜索功能</p>
<p style="line-height: 160%; box-sizing: content-box; margin: 10px 0; color: #333;">点击添加用户按钮进入用户添加页面</p>
<h3 style="line-height: 160%; box-sizing: content-box; font-weight: 700; font-size: 27px; color: #333;">用户添加功能</h3>
<pre style="line-height: 160%; box-sizing: content-box; border: 0; border-radius: 0; margin: 2px 0 8px; background-color: #f5f7f8;"><code style="display: block; overflow-x: auto; background: #1e1e1e; line-height: 160%; box-sizing: content-box; border: 0; border-radius: 0; letter-spacing: -.3px; padding: 18px; color: #f4f4f4; white-space: pre-wrap;">class StuAddView(CreateView):
    template_name = 'stuadd.html'
    model = students
    #自己写modelForm进行表单验证
    form_class = StuModelForm

    def get_success_url(self):
        return reverse('students:list')

    def get_context_data(self, **kwargs):
        context = super(StuAddView, self).get_context_data()
        print(context)
        return context

    def form_invalid(self, form_class):
        print(form_class)
        return self.render_to_response(self.get_context_data(form=form_class))
</code></pre>
<p style="line-height: 160%; box-sizing: content-box; margin: 10px 0; color: #333;">效果图<br/>
<img src="%E7%AC%AC%E5%9B%9B%E6%AC%A1%E4%BD%9C%E4%B8%9A%20%E4%BD%BF%E7%94%A8modelForm%E8%BF%9B%E8%A1%8C%E8%A1%A8%E5%8D%95%E9%AA%8C%E8%AF%81.resources/8A828D82-E54C-41A2-B686-692A5D5A15DB.png" height="588" width="880"/></p>
<p style="line-height: 160%; box-sizing: content-box; margin: 10px 0; color: #333;">该页面实现了对字段的modelForm验证，同时如果密码和确认密码字段不一样，也无法通过验证。</p>
<p style="line-height: 160%; box-sizing: content-box; margin: 10px 0; color: #333;">缺陷：如果表单验证不通过，该页面输入的内容就会消失，如下图：<br/>
<img src="%E7%AC%AC%E5%9B%9B%E6%AC%A1%E4%BD%9C%E4%B8%9A%20%E4%BD%BF%E7%94%A8modelForm%E8%BF%9B%E8%A1%8C%E8%A1%A8%E5%8D%95%E9%AA%8C%E8%AF%81.resources/5D5EBFB3-0455-40C8-9A68-2ADCCEA579C3.png" height="594" width="988"/></p>
<h3 style="line-height: 160%; box-sizing: content-box; font-weight: 700; font-size: 27px; color: #333;">用户更新功能</h3>
<pre style="line-height: 160%; box-sizing: content-box; border: 0; border-radius: 0; margin: 2px 0 8px; background-color: #f5f7f8;"><code style="display: block; overflow-x: auto; background: #1e1e1e; line-height: 160%; box-sizing: content-box; border: 0; border-radius: 0; letter-spacing: -.3px; padding: 18px; color: #f4f4f4; white-space: pre-wrap;">class StuUpdateView(SuccessMessageMixin, UpdateView):
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
        
    def form_valid(self, form):
        messages.success(self.request, '更新成功')
        return super(StuUpdateView,self).form_valid(form)
</code></pre>
<p style="line-height: 160%; box-sizing: content-box; margin: 10px 0; color: #333;"><img src="%E7%AC%AC%E5%9B%9B%E6%AC%A1%E4%BD%9C%E4%B8%9A%20%E4%BD%BF%E7%94%A8modelForm%E8%BF%9B%E8%A1%8C%E8%A1%A8%E5%8D%95%E9%AA%8C%E8%AF%81.resources/F4042492-A338-4576-8DA3-389CD6DBF3A0.png" height="474" width="856"/></p>
<p style="line-height: 160%; box-sizing: content-box; margin: 10px 0; color: #333;">缺陷：在点击保存并继续后，应该在该页面上显示 修改成功字样<br/>
<img src="%E7%AC%AC%E5%9B%9B%E6%AC%A1%E4%BD%9C%E4%B8%9A%20%E4%BD%BF%E7%94%A8modelForm%E8%BF%9B%E8%A1%8C%E8%A1%A8%E5%8D%95%E9%AA%8C%E8%AF%81.resources/CF284794-05FE-475E-B1E9-521FA91E5D57.png" height="360" width="756"/></p>
<h3 style="line-height: 160%; box-sizing: content-box; font-weight: 700; font-size: 27px; color: #333;">用户删除功能</h3>
<pre style="line-height: 160%; box-sizing: content-box; border: 0; border-radius: 0; margin: 2px 0 8px; background-color: #f5f7f8;"><code style="display: block; overflow-x: auto; background: #1e1e1e; line-height: 160%; box-sizing: content-box; border: 0; border-radius: 0; letter-spacing: -.3px; padding: 18px; color: #f4f4f4; white-space: pre-wrap;">class StuDeleteView(DeleteView):
    template_name = 'studelete.html'
    model = students
    context_object_name = "stu"

    def get_success_url(self):
        return reverse('students:list')
</code></pre>
</div><center style="display:none !important;visibility:collapse !important;height:0 !important;white-space:nowrap;width:100%;overflow:hidden"></center></body></html>