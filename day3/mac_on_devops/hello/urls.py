from django.urls import path, re_path
from . import views

urlpatterns = [

    #如果主路由中这么写：path('hello/', include('hello.urls'), name='hello')，那么子路由这么写
    path('', views.index),
    #path('hello/', views.index),

    #如果主路由中这么写：path('hello', include('hello.urls'), name='hello')，那么子路由这么写
    #path('/', views.index),
    #path('/hello/', views.index),

    path('list/', views.my_list, name="list"),
    path('', views.index),
    #关键字传参例子
    #re_path('(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/', views.index),
    #位置传参例子
    #re_path('([0-9]{4})/([0-9]{2})/', views.index),

    path('userlist/', views.userlist),

]