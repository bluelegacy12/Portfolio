"""
URL configuration for trans_comm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from . import views
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^transpo/account/(?P<pk>[0-9]+)/$', views.AccountUpdate.as_view(), name='account-update'),
    re_path(r'^transpo/account/editphoto(?P<pk>[0-9]+)/$', views.UpdateProfilePic.as_view(), name='edit-photo'),
    path('', RedirectView.as_view(pattern_name='home', permanent=False)),
    path('transpo/home', RedirectView.as_view(pattern_name='home', permanent=False)),
    path('accounts/profile/', RedirectView.as_view(pattern_name='home', permanent=False)),
    path('transpo/', views.HomeView.as_view(), name='home'),
    path('transpo/videos', views.Videos.as_view(), name='videos'),
    path('transpo/hashtags', views.Hashtags.as_view(), name='hashtags'),
    path('transpo/login', LoginView.as_view(template_name='login.html'), name='login'),
    path('transpo/logout', LogoutView.as_view(template_name="logout.html"), name='logout'),
    path('transpo/register/', views.UserFormView.as_view(), name='register'),
    path('transpo/post', views.PostCreate.as_view(), name='post'),
    path('transpo/profile', views.ProfileView.as_view(), name='profile'),
    path('transpo/profile/about', views.AboutView.as_view(), name='about'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
