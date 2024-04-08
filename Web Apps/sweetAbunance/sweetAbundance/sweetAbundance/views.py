from django.views import generic
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .forms import NameForm, UserForm, ReviewForm
from .models import *
from django.views.generic.edit import CreateView, DeleteView, UpdateView
import random
import re

class HomeView(generic.ListView):
    template_name = 'home.html'
    model = User

    def get_queryset(self):
        try:
            return User.objects.filter(user=self.request.user)
        except:
            return ""
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        try:
            context['account'] = Account.objects.get(user=self.request.user)
        except:
            context['account'] = ""
        return context
    
class ProfileView(generic.ListView):
    template_name = 'profile.html'
    model = Account

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['account'] = Account.objects.get(user=self.request.user)
        try:
            context['referredBy'] = Account.objects.get(referCode=context['account'].referredBy).user
        except:
            return context
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
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['retype_password']
            if (password != password2):
                return render(request, self.template_name, {'form': form})
            user.set_password(password)
            user.username = username

            # create account data and link it to new user
            account = Account()
            account.user = user
            account.name = username
            account.phone = request.POST.get('phone', False)
            
            # verify and find who referred them, if any referral code was used, and award them points
            referredBy = request.POST.get('referredBy', False)
            if referredBy:
                print(referredBy)
                if referredBy in Account.objects.values_list('referCode', flat=True):
                    account.referredBy = referredBy
                    friend = Account.objects.get(referCode=referredBy)
                    friend.points += 50
                    account.points += 50
                    friend.save()
                else:
                    error = f'Referral code: "{ referredBy }" does not exist'
                    return render(request, self.template_name, {'form': form, 'error': error})

            code = ""
            keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
            
            # generate unique referral code
            while code == "" or code in Account.objects.values_list('referCode', flat=True):
                print(Account.objects.values_list('referCode', flat=True))
                code = ""
                random.shuffle(keys)
                for x in range(6):
                    code += keys[x]
            
            account.referCode = code
            user.save()
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
    
class ShopView(generic.ListView):
    model = Product
    template_name = "shop.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ShopView, self).get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        return context

class ProductView(generic.DetailView):
    model = Product
    template_name = "product.html"

    def get_context_data(self, *args, **kwargs):
        return super(ProductView, self).get_context_data(**kwargs)
    
class ReviewCreate(View):
    template_name = 'createReview.html'
    form_class = ReviewForm

    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'product': Product.objects.get(name=self.request.META['QUERY_STRING'].replace('%20', ' '))})

    #register user based on input data
    def post(self, request):
        review = Review()
        review.rating = request.POST.get('rating')
        review.text = request.POST.get('text')
        review.product = Product.objects.get(name=self.request.META['QUERY_STRING'].replace('%20', ' '))
        review.account = Account.objects.get(user=self.request.user)
        review.save()

        return redirect('product', review.product)


