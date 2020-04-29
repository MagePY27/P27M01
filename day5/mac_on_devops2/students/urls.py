from django.urls import path, re_path

from .views import StuListView, StuAddView, StuUpdateView, StuDeleteView
from .views8 import AddStu, ListStu, DetailStu

app_name = 'students'
urlpatterns = [
    path('list/', StuListView.as_view(), name='list'),
    path('add/', StuAddView.as_view(), name='add'),
    re_path('update/(?P<pk>[0-9]+)?/', StuUpdateView.as_view(), name='update'),
    re_path('delete/(?P<pk>[0-9]+)?/', StuDeleteView.as_view(), name='delete'),

    #通过jQuery实现
    path('jadd/', AddStu.as_view(), name="jadd"),
    path('jlist/', ListStu.as_view(), name='jlist'),
    re_path('jdetail/(?P<pk>[0-9]+)?/',DetailStu.as_view(), name='jdetail'),
]