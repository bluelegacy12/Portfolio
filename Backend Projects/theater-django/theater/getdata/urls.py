from . import views
from django.urls import path, re_path

app_name = 'getdata'

urlpatterns = [
    path('added/', views.home),
    path('home/', views.home),
    # /info/23/
    re_path(r'^info/(?P<performer_id>[0-9]+)/$', views.info, name='info'),
    re_path(r'^info/(?P<show_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    path('register', views.UserFormView.as_view(), name='register'),
]