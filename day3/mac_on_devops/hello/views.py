from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from hello.models import User
import datetime

# Create your views here.
# def index(request):
#     return HttpResponse("<p>Hello Word, Hello Django</p>")
#http://127.0.0.1:8000/hello/?year=2020&month=09
def index1(request):
    print(request.GET) #<QueryDict: {'year': ['2020'], 'month': ['09']}>
    year = request.GET.get('year', '1990')
    mon = request.GET.get('month', '8')
    print(year,mon)
    return HttpResponse("<p>year {}, mon {}</p>".format(year, mon))

# def index(request, *args):
#     print(request, type(request))
#     print(request.body)
#     print(request.GET)
#     year, month=args
#     print(year, month)
#     return HttpResponse("<p>year {}, mon {}</p>".format(year, month))

#关键字传参例子
# #URL http://127.0.0.1:8000/hello/2020/09/
# def index(request, **kwargs):
#     print(kwargs) #{'year': '2020', 'month': '09'}
#     year = kwargs.get('year')
#     month = kwargs.get('month')
#     return HttpResponse("<p>year {}, mon {}</p>".format(year, month))
    #return HttpResponse("<p>Hello Word, Hello Django</p>")

def index(request):
    if request.method == "POST":
        # print('1',request.method)
        # print('2',request.body)
        # print('3',request.POST)
        # print('4', QueryDict(request.body))
        # print('5',QueryDict(request.body).dict())
        print(request.POST)
        print(request.POST.getlist('year'))


    return HttpResponse("<p>Hello Word, Hello Django</p>")


def my_list(request):
    users = [
        {"username":'user1', "name":"user1", "age":18}
    ]
    print(users)
    m_user = User.objects.create(name='user5',password='123')
    d2 = {'name':'zhoushuyu', 'password':'123'}
    User.objects.create(**d2)
    return render(request, 'list.html', {'users':users})


def userlist(request):
    users = [
        {'username': 'kk1', 'name_cn': 'kk1', 'age': 18},
        {'username': 'kk1', 'name_cn': 'kk1', 'age': 18},
        {'username': 'kk1', 'name_cn': 'kk1', 'age': 18},
    ]
    messages = "abc"
    now = datetime.datetime.now()
    return render(request,'userlist.html',{
        'Users': users,
        'messages': messages,
        'now': now
    })