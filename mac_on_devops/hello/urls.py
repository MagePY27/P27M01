from django.urls import path
from . import views

urlpatterns = [

    #如果主路由中这么写：path('hello/', include('hello.urls'), name='hello')，那么子路由这么写
    path('', views.index),
    path('hello/', views.index),

    #如果主路由中这么写：path('hello', include('hello.urls'), name='hello')，那么子路由这么写
    #path('/', views.index),
    #path('/hello/', views.index),

]