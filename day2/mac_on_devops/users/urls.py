from django.urls import path, re_path
from . import views

urlpatterns = [
    path('list/', views.UserList),
    path('add/', views.UserAdd),
    path('edit/', views.UserEdit),
    #path('del/', views.UserDel),
    re_path('del/([1-9]\d*)', views.UserDel), #位置传参

    #re_path('(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/', views.index),
]


#http://127.0.0.1:8000/user/edit/