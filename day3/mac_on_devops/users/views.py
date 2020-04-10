from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import users

# Create your views here.
def UserList(request):
    all_users = users.objects.all
    print(all_users)
    return render(request,'userlist1.html',{
        'all_users': all_users,
    })

def UserAdd(request):
    if request.method == 'POST':
        username = request.POST['username']
        sex = request.POST['sex']
        password = request.POST['password']
        if sex == '男':
            sex = 0
        if sex == '女':
            sex = 1
        # print(username, sex, password)
        data = {'username':username, 'sex':sex, 'password':password}
        users.objects.create(**data)
    return render(request,'useradd.html')
    #return HttpResponseRedirect('/users/list/')

def UserEdit(request):
    if request.method == 'GET':
        #print(request.GET, request.GET.get('user_id'))
        pk = request.GET.get('user_id')
        res = users.objects.get(id=pk)
        print(res)
        print(res.username, res.password, res.sex)
        return render(request, 'useredit.html',{
            'res': res,
        })
    if request.method == 'POST':
        data = request.POST #<QueryDict: {'username': ['user2'], 'sex': ['女'], 'password': ['P@ssw0rd'], 'id': ['1']}>
        sex = 0
        if data['sex'] == '女':
            sex = 1
        if data['sex'] == '男':
            sex = 0
        users.objects.filter(id=data['id']).update(username=data['username'],sex=sex,password=data['password'])
        #return render(request, 'useredit.html')
        #return HttpResponse('{"status":"success"}', content_type='application/json')
        return HttpResponseRedirect('/users/list/')

def UserDel(request, *args, **kwargs):
    # print(request) <WSGIRequest: GET '/users/del/1'>
    #得到前端传递过来的逐渐ID
    pk = args[0]
    print(pk)
    u = users.objects.filter(id=pk).delete()
    #return HttpResponse('{"status":"success"}', content_type='application/json')
    return HttpResponseRedirect('/users/list/')