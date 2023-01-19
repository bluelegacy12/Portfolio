from django.shortcuts import render, get_object_or_404, redirect
from .forms import NameForm, UserForm
from .models import Performers, Shows, Roles, CallTime
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

all_performers = Performers.objects.all()
all_shows = Shows.objects.all()
all_roles = Roles.objects.all()

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
    template_name = 'create_form.html'

class ShowCreate(CreateView):
    model = Shows
    fields = ['title', 'rehearsal_start', 'show_open', 'director_id']
    template_name = 'create_form.html'

class RoleCreate(CreateView):
    model = Roles
    fields = ['name', 'show_id', 'performer_id']
    template_name = 'create_form.html'

class HomeView(generic.ListView):
    template_name = 'home.html'

    def get_queryset(self):
        return Shows.objects.all()

class InfoView(generic.DetailView):
    model = Performers
    template_name = 'info.html'

class ShowInfoView(generic.DetailView):
    model = Shows
    template_name = 'showinfo.html'

class RoleInfoView(generic.DetailView):
    model = Roles
    template_name = 'roleinfo.html'

class PerformerUpdate(UpdateView):
    model = Performers
    fields = ['name', 'email', 'phone']
    template_name = 'create_form.html'

class PerformerDelete(DeleteView):
    model = Performers
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('getdata:home')

class ShowUpdate(UpdateView):
    model = Shows
    fields = ['title', 'rehearsal_start', 'show_open', 'director_id']
    template_name = 'create_form.html'

class ShowDelete(DeleteView):
    model = Shows
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('getdata:home')

class RoleUpdate(UpdateView):
    model = Roles
    fields = ['name', 'show_id', 'performer_id']
    template_name = 'create_form.html'

class RoleDelete(DeleteView):
    model = Roles
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('getdata:home')

class CallCreate(CreateView):
    model = CallTime
    template_name = 'create_form.html'
    fields = ['show_id', 'date', 'start_time', 'end_time', 'performers', 'notes']

class CallInfoView(generic.DetailView):
    model = CallTime
    template_name = 'callinfo.html'