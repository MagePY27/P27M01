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
</div><center style="display:none !important;visibility:collapse !important;height:0 !important;white-space:nowrap;width:100%;overflow:hidden">%0A%23%23%23%20%E7%94%A8%E6%88%B7%E5%B1%95%E7%A4%BA%E5%8A%9F%E8%83%BD%0A%60%60%60%0Aclass%20StuListView(TemplateView)%3A%0A%20%20%20%20template_name%20%3D%20'stulist.html'%0A%20%20%20%20model%20%3D%20students%0A%0A%20%20%20%20def%20get_context_data(self%2C%20**kwargs)%3A%0A%20%20%20%20%20%20%20%20context%20%3D%20super(StuListView%2Cself).get_context_data(**kwargs)%0A%20%20%20%20%20%20%20%20context%5B%22all_students%22%5D%20%3D%20students.objects.all()%0A%20%20%20%20%20%20%20%20return%20context%0A%60%60%60%0A%0A%E8%AE%BF%E9%97%AEURL%0Ahttp%3A%2F%2F127.0.0.1%3A9000%2Fstudents%2Flist%2F%0A%E6%95%88%E6%9E%9C%E5%9B%BE%0A!%5B4ebeb210042b3ea9e07be6031c5b7efe.png%5D(evernotecid%3A%2F%2FBA30DB65-67D6-4761-A907-0CB104C2E14B%2Fappyinxiangcom%2F18707421%2FENResource%2Fp720)%0A%0A%E7%BC%BA%E9%99%B7%EF%BC%9A%E7%9B%AE%E5%89%8D%E6%9C%AA%E5%AE%9E%E7%8E%B0%E6%90%9C%E7%B4%A2%E5%8A%9F%E8%83%BD%0A%0A%E7%82%B9%E5%87%BB%E6%B7%BB%E5%8A%A0%E7%94%A8%E6%88%B7%E6%8C%89%E9%92%AE%E8%BF%9B%E5%85%A5%E7%94%A8%E6%88%B7%E6%B7%BB%E5%8A%A0%E9%A1%B5%E9%9D%A2%0A%0A%23%23%23%20%E7%94%A8%E6%88%B7%E6%B7%BB%E5%8A%A0%E5%8A%9F%E8%83%BD%0A%60%60%60%0Aclass%20StuAddView(CreateView)%3A%0A%20%20%20%20template_name%20%3D%20'stuadd.html'%0A%20%20%20%20model%20%3D%20students%0A%20%20%20%20%23%E8%87%AA%E5%B7%B1%E5%86%99modelForm%E8%BF%9B%E8%A1%8C%E8%A1%A8%E5%8D%95%E9%AA%8C%E8%AF%81%0A%20%20%20%20form_class%20%3D%20StuModelForm%0A%0A%20%20%20%20def%20get_success_url(self)%3A%0A%20%20%20%20%20%20%20%20return%20reverse('students%3Alist')%0A%0A%20%20%20%20def%20get_context_data(self%2C%20**kwargs)%3A%0A%20%20%20%20%20%20%20%20context%20%3D%20super(StuAddView%2C%20self).get_context_data()%0A%20%20%20%20%20%20%20%20print(context)%0A%20%20%20%20%20%20%20%20return%20context%0A%0A%20%20%20%20def%20form_invalid(self%2C%20form_class)%3A%0A%20%20%20%20%20%20%20%20print(form_class)%0A%20%20%20%20%20%20%20%20return%20self.render_to_response(self.get_context_data(form%3Dform_class))%0A%60%60%60%0A%E6%95%88%E6%9E%9C%E5%9B%BE%0A!%5B96e647e30eefd71abb99a869a87bb34d.png%5D(evernotecid%3A%2F%2FBA30DB65-67D6-4761-A907-0CB104C2E14B%2Fappyinxiangcom%2F18707421%2FENResource%2Fp721)%0A%0A%E8%AF%A5%E9%A1%B5%E9%9D%A2%E5%AE%9E%E7%8E%B0%E4%BA%86%E5%AF%B9%E5%AD%97%E6%AE%B5%E7%9A%84modelForm%E9%AA%8C%E8%AF%81%EF%BC%8C%E5%90%8C%E6%97%B6%E5%A6%82%E6%9E%9C%E5%AF%86%E7%A0%81%E5%92%8C%E7%A1%AE%E8%AE%A4%E5%AF%86%E7%A0%81%E5%AD%97%E6%AE%B5%E4%B8%8D%E4%B8%80%E6%A0%B7%EF%BC%8C%E4%B9%9F%E6%97%A0%E6%B3%95%E9%80%9A%E8%BF%87%E9%AA%8C%E8%AF%81%E3%80%82%0A%0A%E7%BC%BA%E9%99%B7%EF%BC%9A%E5%A6%82%E6%9E%9C%E8%A1%A8%E5%8D%95%E9%AA%8C%E8%AF%81%E4%B8%8D%E9%80%9A%E8%BF%87%EF%BC%8C%E8%AF%A5%E9%A1%B5%E9%9D%A2%E8%BE%93%E5%85%A5%E7%9A%84%E5%86%85%E5%AE%B9%E5%B0%B1%E4%BC%9A%E6%B6%88%E5%A4%B1%EF%BC%8C%E5%A6%82%E4%B8%8B%E5%9B%BE%EF%BC%9A%0A!%5B28ec75e85fa872b0398e5b4e9e29fa38.png%5D(evernotecid%3A%2F%2FBA30DB65-67D6-4761-A907-0CB104C2E14B%2Fappyinxiangcom%2F18707421%2FENResource%2Fp722)%0A%0A%23%23%23%20%E7%94%A8%E6%88%B7%E6%9B%B4%E6%96%B0%E5%8A%9F%E8%83%BD%0A%60%60%60%0Aclass%20StuUpdateView(SuccessMessageMixin%2C%20UpdateView)%3A%0A%20%20%20%20template_name%20%3D%20'stuupdate.html'%0A%20%20%20%20model%20%3D%20students%0A%20%20%20%20%23fields%20%3D%20%22__all__%22%0A%20%20%20%20context_object_name%20%3D%20%22stu%22%0A%20%20%20%20form_class%20%3D%20StuModelForm%0A%20%20%20%20'''%E5%A6%82%E6%9E%9Cfields%E5%92%8Cform_class%E5%90%8C%E6%97%B6%E6%89%93%E5%BC%80%E4%BC%9A%E6%8A%A5%E5%A6%82%E4%B8%8B%E9%94%99%E8%AF%AF%EF%BC%9B%E5%9B%A0%E4%B8%BAfields%E8%B5%B0%E7%9A%84%E6%98%AF%E7%B3%BB%E7%BB%9F%E7%9A%84model%20form%E9%AA%8C%E8%AF%81%EF%BC%8Cform_class%E8%B5%B0%E7%9A%84%E6%98%AF%E8%87%AA%E5%AE%9A%E4%B9%89%E7%9A%84model%20form%E9%AA%8C%E8%AF%81'''%0A%20%20%20%20'''Specifying%20both%20'fields'%20and%20'form_class'%20is%20not%20permitted.'''%0A%20%20%20%20success_message%20%3D%20%22%E6%9B%B4%E6%96%B0%E6%88%90%E5%8A%9F%22%0A%20%20%20%20%23success_message%20%3D%20%22%25(name)s%20update%20successfully%22%0A%0A%20%20%20%20def%20get_success_url(self)%3A%0A%20%20%20%20%20%20%20%20print('StuUpdateView%20request.POST%E6%98%AF%EF%BC%9A'%2Cself.request.POST)%0A%20%20%20%20%20%20%20%20print('StuUpdateView%20self.__dict__'%2C%20self.__dict__)%0A%20%20%20%20%20%20%20%20if%20'_continue'%20in%20self.request.POST%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20return%20reverse('students%3Aupdate'%2C%20kwargs%3D%7B'pk'%3A%20self.__dict__%5B'kwargs'%5D%5B'pk'%5D%7D)%0A%20%20%20%20%20%20%20%20return%20reverse('students%3Alist')%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20def%20form_valid(self%2C%20form)%3A%0A%20%20%20%20%20%20%20%20messages.success(self.request%2C%20'%E6%9B%B4%E6%96%B0%E6%88%90%E5%8A%9F')%0A%20%20%20%20%20%20%20%20return%20super(StuUpdateView%2Cself).form_valid(form)%0A%60%60%60%0A!%5Bd71992c643c7db7d0f1feb5fcad65907.png%5D(evernotecid%3A%2F%2FBA30DB65-67D6-4761-A907-0CB104C2E14B%2Fappyinxiangcom%2F18707421%2FENResource%2Fp723)%0A%0A%E7%BC%BA%E9%99%B7%EF%BC%9A%E5%9C%A8%E7%82%B9%E5%87%BB%E4%BF%9D%E5%AD%98%E5%B9%B6%E7%BB%A7%E7%BB%AD%E5%90%8E%EF%BC%8C%E5%BA%94%E8%AF%A5%E5%9C%A8%E8%AF%A5%E9%A1%B5%E9%9D%A2%E4%B8%8A%E6%98%BE%E7%A4%BA%20%E4%BF%AE%E6%94%B9%E6%88%90%E5%8A%9F%E5%AD%97%E6%A0%B7%0A!%5B96064bef3f62d3df9923f25021209afa.png%5D(evernotecid%3A%2F%2FBA30DB65-67D6-4761-A907-0CB104C2E14B%2Fappyinxiangcom%2F18707421%2FENResource%2Fp724)%0A%0A%23%23%23%20%E7%94%A8%E6%88%B7%E5%88%A0%E9%99%A4%E5%8A%9F%E8%83%BD%0A%60%60%60%0Aclass%20StuDeleteView(DeleteView)%3A%0A%20%20%20%20template_name%20%3D%20'studelete.html'%0A%20%20%20%20model%20%3D%20students%0A%20%20%20%20context_object_name%20%3D%20%22stu%22%0A%0A%20%20%20%20def%20get_success_url(self)%3A%0A%20%20%20%20%20%20%20%20return%20reverse('students%3Alist')%0A%60%60%60%0A%0A%0A%0A</center></body></html>