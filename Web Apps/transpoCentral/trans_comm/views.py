from typing import Any
from django.db.models.query import QuerySet
from django.views import generic
from django.views.generic import View
from .models import User, Post, Account
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .forms import NameForm, UserForm
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import PhotoForm
import re

class UpdateProfilePic(generic.UpdateView):
    template_name = 'photo_list.html'
    model = Account
    fields = ['profilePic']

    def photo_list(request):
        photo = 'test'
        if request.method == 'POST':
            form = PhotoForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('photo_list')
        else:
            form = PhotoForm()
            return render(request, 'photo_list.html', {'form': form, 'photo': photo})

    def get_form(self, *args, **kwargs):
        form = super(UpdateProfilePic, self).get_form(*args, **kwargs)
        return form
    
    def get_context_data(self, **kwargs):
        context = super(UpdateProfilePic, self).get_context_data(**kwargs)
        context['account'] = Account.objects.get(user=self.request.user)
        return context

class HomeView(generic.ListView):
    template_name = 'home.html'
    model = Post

    def get_queryset(self):
        return Post.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        try:
            context['account'] = Account.objects.get(user=self.request.user)
        except:
            context['account'] = ""
        return context

class Videos(generic.ListView):
    template_name = 'videos.html'
    model = Post

    def get_queryset(self):
        return Post.objects.exclude(video__exact='')
    
    def get_context_data(self, **kwargs):
        context = super(Videos, self).get_context_data(**kwargs)
        context['account'] = Account.objects.get(user=self.request.user)
        return context
    
class Hashtags(generic.ListView):
    template_name = 'hashtags.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(text__icontains="#")
    
    def get_context_data(self, **kwargs):
        context = super(Hashtags, self).get_context_data(**kwargs)
        hashtagPosts = Post.objects.filter(text__icontains="#")
        context['hashtags'] = []
        hashtagCounters = {}
        for post in hashtagPosts:
            hashtags = re.findall(r"#(\w+)", post.text)
            for hashtag in hashtags:
                if hashtag not in hashtagCounters:
                    hashtagCounters[hashtag] = 1
                else:
                    hashtagCounters[hashtag] += 1          
        sortedHashtags = dict(sorted(hashtagCounters.items(), key=lambda x:x[1], reverse=True))
        for entry in sortedHashtags:
            context['hashtags'].append(entry)
        return context
    
    def get_context_data(self, **kwargs):
        context = super(Hashtags, self).get_context_data(**kwargs)
        context['account'] = Account.objects.get(user=self.request.user)
        return context
        
class ProfileView(generic.ListView):
    template_name = 'profile.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['account'] = Account.objects.get(user=self.request.user)
        return context
    
class AboutView(generic.ListView):
    template_name = 'about.html'
    model = User

    def get_queryset(self):
        return User.objects.get(username=self.request.user.username)
    
    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['account'] = Account.objects.get(user=self.request.user)
        return context
    
class UserFormView(View):
    form_class = UserForm
    template_name = 'register.html'

    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    #register user based on input data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # unify the data into commit-ready format (cleaned data or normalized)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['retype_password']
            if (password != password2):
                return render(request, self.template_name, {'form': form})
            user.set_password(password)
            user.save()
            account = Account()
            account.user = user
            account.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
        return render(request, self.template_name, {'form': form})
    
    def get_context_data(self, **kwargs):
        context = super(UserFormView, self).get_context_data(**kwargs)
        context['account'] = Account.objects.get(user=self.request.user)
        return context
    
class PostCreate(generic.ListView):
    template_name = 'home.html'

    def get_queryset(self):
        return User.objects.get(username=self.request.user.username)

    def post(self, request):
        post = Post()
        post.user = self.request.user
        post.text=request.POST.get('text')
        post.save()
        return redirect('home')
    
    def get_context_data(self, **kwargs):
        context = super(PostCreate, self).get_context_data(**kwargs)
        context['account'] = Account.objects.get(user=self.request.user)
        return context
    
class AccountUpdate(generic.UpdateView):
    template_name = 'create_form.html'
    model = Account
    fields = ['profilePic', 'bannerPic', 'worksAt', 'livesIn', 'whereFrom', 'occupation']

    def get_form(self, *args, **kwargs):
        form = super(AccountUpdate, self).get_form(*args, **kwargs)
        return form
    
    def get_context_data(self, **kwargs):
        context = super(AccountUpdate, self).get_context_data(**kwargs)
        context['account'] = Account.objects.get(user=self.request.user)
        return context
    
