from . import views
from django.urls import path, re_path
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'getdata'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('venues/', views.VenueView.as_view(), name='venues'),
    path('user/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='home.html'), name='logout'),
    path('documents/', views.UploadsView.as_view(), name='documents'),
    # /info/23/
    re_path(r'^info/(?P<pk>[0-9]+)/$', views.InfoView.as_view(), name='info'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('privacy/', views.PrivacyChange.as_view(), name='privacy'),
    path('alert/', views.SendAlert.as_view(), name='alert'),
    path('user/register/', views.UserFormView.as_view(), name='register'),
    path('user/registercompany/', views.CompanyFormView.as_view(), name='registercompany'),
    path('performer/add/', views.AddPerformer.as_view(), name='add-performer'),
    path('show/add/', views.ShowCreate.as_view(), name='show-add'),
    path('role/add/', views.RoleCreate.as_view(), name='role-add'),
    path('call/add/', views.CallCreate.as_view(), name='call-add'),
    path('venue/add/', views.VenueCreate.as_view(), name='venue-add'),
    path('documents/add/', views.UploadsCreate.as_view(), name='documents-add'),
    path('schedule/', views.CreatePDF.as_view(), name='schedule'),
    re_path(r'^showinfo/(?P<pk>[0-9]+)/$', views.ShowInfoView.as_view(), name='showinfo'),
    re_path(r'^roleinfo/(?P<pk>[0-9]+)/$', views.RoleInfoView.as_view(), name='roleinfo'),
    re_path(r'^callinfo/(?P<pk>[0-9]+)/$', views.CallInfoView.as_view(), name='callinfo'),
    re_path(r'^venueinfo/(?P<pk>[0-9]+)/$', views.VenueInfoView.as_view(), name='venueinfo'),
    re_path(r'^venue/(?P<pk>[0-9]+)/$', views.VenueUpdate.as_view(), name='venue-update'),
    re_path(r'^venue/(?P<pk>[0-9]+)/delete/$', views.VenueDelete.as_view(), name='venue-delete'),
    re_path(r'^call/(?P<pk>[0-9]+)/$', views.CallUpdate.as_view(), name='call-update'),
    re_path(r'^call/(?P<pk>[0-9]+)/delete/$', views.CallDelete.as_view(), name='call-delete'),
    re_path(r'^performer/(?P<pk>[0-9]+)/$', views.PerformerUpdate.as_view(), name='performer-update'),
    # re_path(r'^performer/(?P<pk>[0-9]+)/delete/$', views.PerformerDelete.as_view(), name='performer-delete'),
    re_path(r'^documents/(?P<pk>[0-9]+)/$', views.UploadsUpdate.as_view(), name='documents-update'),
    re_path(r'^documents/(?P<pk>[0-9]+)/delete/$', views.UploadsDelete.as_view(), name='documents-delete'),
    re_path(r'^show/(?P<pk>[0-9]+)/$', views.ShowUpdate.as_view(), name='show-update'),
    re_path(r'^show/(?P<pk>[0-9]+)/delete/$', views.ShowDelete.as_view(), name='show-delete'),
    re_path(r'^role/(?P<pk>[0-9]+)/$', views.RoleUpdate.as_view(), name='role-update'),
    re_path(r'^role/(?P<pk>[0-9]+)/delete/$', views.RoleDelete.as_view(), name='role-delete'),
    re_path(r'^company/(?P<pk>[0-9]+)/$', views.CompanyUpdate.as_view(), name='company-update'),
]