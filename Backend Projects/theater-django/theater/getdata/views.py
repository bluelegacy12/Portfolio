from django.shortcuts import render, get_object_or_404, redirect
from .forms import NameForm, UserForm
from .models import Performers, Shows, Roles, CallTime, RehearsalVenues, Uploads
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group

all_performers = Performers.objects.all()
all_shows = Shows.objects.all()
all_roles = Roles.objects.all()

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
            user.set_password(password)
            user.save()
            group = Group.objects.get(name='Artist')
            user.groups.add(group)

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('getdata:home')
        return render(request, self.template_name, {'form': form})

class CompanyFormView(View):
    form_class = UserForm
    template_name = 'company_register.html'

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
            user.set_password(password)
            user.save()
            group = Group.objects.get(name='Company')
            user.groups.add(group)

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
    fields = ['show_id_id', 'venue_id', 'date', 'start_time', 'end_time', 'performers', 'notes']

class CallInfoView(generic.DetailView):
    model = CallTime
    template_name = 'callinfo.html'

    def get_context_data(self, **kwargs):
        context = super(CallInfoView, self).get_context_data(**kwargs)
        context['calltimes'] = CallTime.objects.all()
        return context

class CallUpdate(UpdateView):
    model = CallTime
    fields = ['show_id_id', 'venue_id', 'date', 'start_time', 'end_time', 'performers', 'notes']
    template_name = 'create_form.html'

class CallDelete(DeleteView):
    model = CallTime
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('getdata:home')

class VenueView(generic.ListView):
    template_name = 'venues.html'

    def get_queryset(self):
        return RehearsalVenues.objects.all()

class VenueCreate(CreateView):
    model = RehearsalVenues
    fields = ['name', 'location']
    template_name = 'create_form.html'

class VenueInfoView(generic.DetailView):
    model = RehearsalVenues
    template_name = 'venueinfo.html'

class VenueUpdate(UpdateView):
    model = RehearsalVenues
    fields = ['name', 'location']
    template_name = 'create_form.html'

class VenueDelete(DeleteView):
    model = RehearsalVenues
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('getdata:venues')

class UploadsView(generic.ListView):
    template_name = 'documents.html'

    def get_queryset(self):
        return Uploads.objects.all()

class UploadsCreate(CreateView):
    model = Uploads
    fields = ['name', 'file', 'details']
    template_name = 'create_form.html'

class UploadsUpdate(UpdateView):
    model = Uploads
    fields = ['name', 'file', 'details']
    template_name = 'create_form.html'

class UploadsDelete(DeleteView):
    model = Uploads
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('getdata:documents')

