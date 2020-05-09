from django.urls import path, re_path

from . import views, group

app_name = 'users'
urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('add/', views.UserAddView.as_view(), name='add'),
    path('list/', views.UserListView.as_view(), name='list'),
    re_path('modify/(?P<pk>[0-9]+)?/', views.UserUpdateView.as_view(), name='update'),
    re_path('delete/(?P<pk>[0-9]+)?/', views.UserDeleteView.as_view(), name='delete'),

    path('permission/', group.PermListView.as_view(), name='perm_list')
]