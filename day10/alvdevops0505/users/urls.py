from django.urls import path, re_path

from . import views, group

app_name = 'users'
urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('add/', views.UserAddView.as_view(), name='add'),
    path('list/', views.UserListView.as_view(), name='list'),
    re_path('modify/(?P<pk>[0-9]+)?/', views.UserUpdateView.as_view(), name='modify'),
    re_path('user_delete/(?P<pk>[0-9]+)?/', views.UserDeleteView.as_view(), name='del'),
    #re_path('delete/(?P<pk>[0-9]+)?/', views.UserDeleteView.as_view(), name='delete'),
    #2020-05-15
    re_path('user_group/(?P<pk>[0-9]+)?/', views.UserGroupView.as_view(), name='user_group'),
    #2020-05-16T
    re_path('user_perm/(?P<pk>[0-9]+)?/', views.UserPermissionUpdateView.as_view(), name='user_perm_update'),
    re_path('reset_password/(?P<pk>[0-9]+)?/', views.ResetPasswordView.as_view(), name='reset_password'),


    path('permission/', group.PermListView.as_view(), name='perm_list'),
    path('permission_add/', group.PermAddView.as_view(), name='perm_add'),
    re_path('permission_update/(?P<pk>[0-9]+)?/', group.PermUpdateView.as_view(), name='perm_update'),

    path('group/', group.GroupListView.as_view(), name='group_list'),
    path('group_add/', group.GroupAddView.as_view(), name='group_add'),
    re_path('group_update/(?P<pk>[0-9]+)?/', group.GroupUpdateView.as_view(), name='group_update'),
    re_path('group_delete/(?P<pk>[0-9]+)?/', group.GroupDeleteView.as_view(), name='group_delete'),
    re_path('group_add_user/(?P<pk>[0-9]+)?/', group.AddUserToGroupView.as_view(), name='group_add_user')
]