from django.shortcuts import render, get_object_or_404, redirect
from .forms import NameForm, UserForm
from .models import Performers, Shows, Roles
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

all_performers = Performers.objects.all()
all_shows = Shows.objects.all()
all_roles = Roles.objects.all()

def info(request, performer_id):
    p = get_object_or_404(Performers, pk=performer_id)
    performer = all_performers[int(performer_id) - 1] # all_performers is zero indexed, sql pks are not. Must subtract 1 from index
    context = {
        'all_performers': all_performers,
        'performer_id': performer_id,
        'performer': performer,
    }
    return render(request, 'info.html', context)


def addCast(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    return render(request, "added.html", {'name': name}, {'email': email}, {'phone': phone})

def home(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        name = form.get_initial_for_field(name, "Name: name")
        email = form.email
        phone = form.phone
        context = {
            'form': form,
            'name': name,
            'email': email,
            'phone': phone
        }
        performer = Performers.save(name=name, email=email, phone=phone)
        if form.is_valid():
            return render(request, 'added.html', context)

    else:
        form = NameForm()
        context = {
            'all_performers': all_performers,
            'form': form,
            'all_roles': all_roles,
            'all_shows': all_shows,
        }   
    return render(request, 'home.html', context)

def favorite(request, show_id):
    show = get_object_or_404(Shows, pk=show_id)
    try:
        selected_show = Shows.objects.get(pk=request.POST['show'])
    except (KeyError, Shows.DoesNotExist):
        return render(request, 'home.html', {
            'show': show,
            'error_message': "You did not select a valid show"
        })
    else:
        selected_show.favorite = True
        selected_show.save()
        form = NameForm()
        context = {
            'all_performers': all_performers,
            'form': form,
            'all_roles': all_roles,
            'all_shows': all_shows,
        }   
    return render(request, 'home.html', context)

class UserFormView(View):
    form_class = UserForm
    template_name = 'getapp/register.html'

    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    #register user based on input data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # unify the data into commit-ready format
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('getdata:home')
        return render(request, self.template_name, {'form': form})

class PerformerCreate(CreateView):
    model = Performers
    fields = ['name', 'email', 'phone']