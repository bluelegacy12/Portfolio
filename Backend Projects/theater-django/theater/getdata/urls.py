from . import views
from django.urls import path, re_path

urlpatterns = [
    path('added/', views.home),
    path('home/', views.home),
    # /info/23/
    re_path(r'^info/(?P<performer_id>[0-9]+)/$', views.info, name='info')
]