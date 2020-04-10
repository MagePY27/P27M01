from django.urls import path, re_path
from cusers.views import CuserList, CuserAdd, CuserEdit, CuserDel

app_name = 'cusers'
urlpatterns = [
    path('list/', CuserList.as_view(), name='clist'),
    path('add/', CuserAdd.as_view(), name='cadd'),
    path('edit/(?<pk>[0-9]+)?/', CuserEdit.as_view(), name='cedit'),
    path('del/(?<pk>[0-9]+)?/', CuserDel.as_view(), name='cdel')
]