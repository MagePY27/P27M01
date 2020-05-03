from django.shortcuts import render
from django.views.generic import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import students

class VLogin(View):
    def get(self, request):
        return render(request,'admin_3/login.html')


class VList(View):
    def get(self, request):
        all_students = students.objects.all()

        #实现分页效果
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_students, 6, request=request)

        all_students = p.page(page)

        return render(request, 'admin_3/tables-editable.html', {
            'all_students': all_students,
        })