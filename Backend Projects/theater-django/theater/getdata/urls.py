from . import views
from django.urls import path, re_path

app_name = 'getdata'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    # /info/23/
    re_path(r'^info/(?P<pk>[0-9]+)/$', views.InfoView.as_view(), name='info'),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('performers/add/', views.PerformerCreate.as_view(), name='performer-add'),
    path('show/add/', views.ShowCreate.as_view(), name='show-add'),
    path('role/add/', views.RoleCreate.as_view(), name='role-add'),
    re_path(r'^showinfo/(?P<pk>[0-9]+)/$', views.ShowInfoView.as_view(), name='showinfo'),
    re_path(r'^roleinfo/(?P<pk>[0-9]+)/$', views.RoleInfoView.as_view(), name='roleinfo'),
]