from django.urls import path, re_path

from . import views

app_name = 'cmdb'
urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('types/', views.TypeListView.as_view(), name='types'),
    path('types_add/', views.TypeAddView.as_view(), name='type-add'),
    re_path('types_edit/(?P<pk>[0-9]+)?/', views.TypeEditView.as_view(), name='type-edit'),
    re_path('types_delete/(?P<pk>[0-9]+)?/', views.TypeDeleteView.as_view(), name='type-delete'),

    path('tags/', views.TagListView.as_view(), name='tags'),
    path('tags_add/', views.TagAddView.as_view(), name='tag-add'),
    re_path('tags_edit/(?P<pk>[0-9]+)?/', views.TagEditView.as_view(), name='tag-edit'),
    re_path('tags_delete/(?P<pk>[0-9]+)?/', views.TagDeleteView.as_view(), name='tag-delete'),

    path('hosts/', views.HostListView.as_view(), name='hosts'),
    re_path('hosts_tags_add/(?P<pk>[0-9]+)?/', views.HostTagAddView.as_view(), name='host-tags-add'),
    re_path('tags_addhosts/(?P<pk>[0-9]+)?/', views.HostAddByTagView.as_view(), name='add-hosts'),

    path('update_host_info/', views.update_host_info, name='update-host-info'),
    #overview
    path('overview/', views.AssetsOverView.as_view(), name='overview'),
]