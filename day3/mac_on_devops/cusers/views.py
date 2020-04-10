from django.shortcuts import render, HttpResponse

from django.views.generic import View

from users.models import users

import traceback

# Create your views here.
class CuserList(View):
    def get(self,request):
        all_users = users.objects.all()
        return render(request, 'cusers/cuserlist.html', {"all_users":all_users})

    def post(self, request):
        #print(request.POST)
        keyword = request.POST.get('keyword')
        all_users = users.objects.filter(username__contains=keyword)

        return render(request, 'cusers/cuserlist.html', {
            "keyword": keyword,
            "all_users": all_users,
        })
        #return HttpResponse('Hello')

class CuserAdd(View):
    def get(self,request):
        print(request.GET)
        return render(request, 'cusers/cuseradd.html')

    def post(self,request):
        print(request.POST.dict())
        #msg = {}
        try:
            users.objects.create(**request.POST.dict())
            msg = {"code":0, "result":"用户添加成功"}
        except:
            msg = {"code":1, "errmsg":"用户添加失败：%s" %traceback.format_exc()}
        return render(request, 'cusers/cuseradd.html', {
            "msg": msg,
        })


class CuserEdit(View):
    def get(self,request, **kwargs):
        pk = kwargs.get('pk')
        user = users.objects.get(id=pk)
        print(user.username, user.password, user.sex)
        return render(request, 'cusers/cuseredit.html', {'user':user})

    def post(self,request, **kwargs):
        #print(request.POST.dict(), kwargs) #{'username': 'user9', 'password': 'P@ssw0rd', 'sex': '1'} {'pk': '3'}
        try:
            users.objects.filter(id=kwargs['pk']).update(**request.POST.dict())
            msg = {"code":0, "result":"更新用户成功"}
            user = users.objects.get(id=kwargs['pk'])

        except:
            msg = {"code":1, "errmsg":"更新用户失败: %s" % traceback.format_exc()}
        return render(request, 'cusers/cuseredit.html', {"msg":msg, "user":user})

class CuserDel(View):
    def get(self,request, **kwargs):
        try:
            user = users.objects.get(id=kwargs['pk'])
            print(user)
            msg = {}
        except:
            msg = {"code": 1, "errmsg": "用户不存在: %s" % traceback.format_exc()}
        return render(request, 'cusers/cuserdel.html', {"user": user, "msg":msg})
    def post(self,request, **kwargs):
        try:
            user = users.objects.get(id=kwargs['pk'])
            user.delete()
            msg = {"code":0, "result":"删除用户成功"}
        except:
            msg = {"code": 1, "errmsg": "删除用户失败: %s" % traceback.format_exc()}

        return render(request, 'cusers/cuserdel.html', {"user":user, "msg":msg})