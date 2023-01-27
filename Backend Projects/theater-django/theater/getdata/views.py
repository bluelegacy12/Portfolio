from django.shortcuts import render, get_object_or_404, redirect
from .forms import NameForm, UserForm, AddPerformerForm
from .models import Performers, Shows, Roles, CallTime, RehearsalVenues, Uploads, Company
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.http import Http404

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
            password2 = form.cleaned_data['retype_password']
            if (password != password2):
                return render(request, self.template_name, {'form': form})
            user.set_password(password)
            user.save()
            group = Group.objects.get(name='Artist')
            user.groups.add(group)
            performer = Performers()
            performer.username = username
            performer.name = form.cleaned_data['name']
            performer.email = form.cleaned_data['email']
            performer.save()

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
            password2 = form.cleaned_data['retype_password']
            if (password != password2):
                return render(request, self.template_name, {'form': form})
            user.set_password(password)
            user.save()
            group = Group.objects.get(name='Company')
            user.groups.add(group)
            company = Company()
            company.username = username
            company.name = form.cleaned_data['name']
            company.email = form.cleaned_data['email']
            company.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('getdata:home')
        return render(request, self.template_name, {'form': form})

class CompanyUpdate(UpdateView):
    model = Company
    fields = [ 'email', 'performers']
    template_name = 'create_form.html'

    def get_form(self, *args, **kwargs):
        form = super(CompanyUpdate, self).get_form(*args, **kwargs)
        c = Company.objects.get(username=self.request.user.username)
        form.fields['performers'].queryset = c.performers
        return form


def ChangeShowPerformers(self):
    c = Company.objects.get(username=self.request.user.username)
    for show in c.shows_set.all():
        for role in show.roles_set.all():
            if role.performer_id not in c.performers.all():
                role.delete()
    for call in c.calltime_set.all():
        for performer in call.performers.all():
            if performer not in c.performers.all():
                call.performers.remove(performer)
    return

class ShowCreate(CreateView):
    model = Shows
    fields = ['title', 'rehearsal_start', 'show_open', 'director_id', 'company']
    template_name = 'create_form.html'

    def get_form(self, *args, **kwargs):
        form = super(ShowCreate, self).get_form(*args, **kwargs)
        c = Company.objects.get(username=self.request.user.username)
        form.fields['director_id'].queryset = c.performers
        return form

    def get_context_data(self, **kwargs):
        context = super(ShowCreate, self).get_context_data(**kwargs)
        context['companies'] = Company.objects.all()
        return context

class RoleCreate(CreateView):
    model = Roles
    fields = ['name', 'show_id', 'performer_id']
    template_name = 'create_form.html'

    def get_form(self, *args, **kwargs):
        form = super(RoleCreate, self).get_form(*args, **kwargs)
        c = Company.objects.get(username=self.request.user.username)
        form.fields['show_id'].queryset = c.shows_set.all()
        form.fields['performer_id'].queryset = c.performers
        return form

class HomeView(generic.ListView):
    template_name = 'home.html'

    def get_queryset(self):
        return Company.objects.all()

class InfoView(generic.DetailView):
    model = Performers
    template_name = 'info.html'

    def get_context_data(self, **kwargs):
        context = super(InfoView, self).get_context_data(**kwargs)
        context['performer_list'] = Performers.objects.all()
        context['company_list'] = Company.objects.all()
        return context

class ProfileView(generic.ListView):
    template_name = 'profile.html'

    def get_queryset(self):
        for g in self.request.user.groups.all():
            if g.name == "Artist":
                return Performers.objects.get(username=self.request.user.username)
            elif g.name == "Company":
                ChangeShowPerformers(self)
                return Company.objects.get(username=self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['performer_list'] = Performers.objects.all()
        context['company_list'] = Company.objects.all()
        return context

class ShowInfoView(generic.DetailView):
    model = Shows
    template_name = 'showinfo.html'

class RoleInfoView(generic.DetailView):
    model = Roles
    template_name = 'roleinfo.html'

class PerformerUpdate(UpdateView):
    model = Performers
    fields = ['email', 'phone']
    template_name = 'update_performer.html'


class PerformerDelete(DeleteView):
    model = Performers
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('getdata:home')

class ShowUpdate(UpdateView):
    model = Shows
    fields = ['title', 'rehearsal_start', 'show_open', 'director_id']
    template_name = 'create_form.html'

    def get_form(self, *args, **kwargs):
        form = super(ShowUpdate, self).get_form(*args, **kwargs)
        c = Company.objects.get(username=self.request.user.username)
        form.fields['director_id'].queryset = c.performers
        return form

class ShowDelete(DeleteView):
    model = Shows
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('getdata:home')

class RoleUpdate(UpdateView):
    model = Roles
    fields = ['name', 'show_id', 'performer_id']
    template_name = 'create_form.html'

    def get_form(self, *args, **kwargs):
        form = super(RoleUpdate, self).get_form(*args, **kwargs)
        c = Company.objects.get(username=self.request.user.username)
        form.fields['show_id'].queryset = c.shows_set.all()
        form.fields['performer_id'].queryset = c.performers
        return form

class RoleDelete(DeleteView):
    model = Roles
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('getdata:home')

class CallCreate(CreateView):
    model = CallTime
    template_name = 'create_form.html'
    fields = ['show_id_id', 'venue_id', 'date', 'start_time', 'end_time', 'performers', 'notes', 'company']

    def get_form(self, *args, **kwargs):
        form = super(CallCreate, self).get_form(*args, **kwargs)
        c = Company.objects.get(username=self.request.user.username)
        form.fields['show_id_id'].queryset = Shows.objects.filter(company=c.id)
        form.fields['venue_id'].queryset = RehearsalVenues.objects.filter(company=c.id)
        form.fields['performers'].queryset = c.performers
        return form

    def get_context_data(self, **kwargs):
        context = super(CallCreate, self).get_context_data(**kwargs)
        context['companies'] = Company.objects.all()
        return context

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

    def get_form(self, *args, **kwargs):
        form = super(CallUpdate, self).get_form(*args, **kwargs)
        c = Company.objects.get(username=self.request.user.username)
        form.fields['show_id_id'].queryset = Shows.objects.filter(company=c.id)
        form.fields['venue_id'].queryset = RehearsalVenues.objects.filter(company=c.id)
        form.fields['performers'].queryset = c.performers
        return form

class CallDelete(DeleteView):
    model = CallTime
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('getdata:home')

class VenueView(generic.ListView):
    template_name = 'venues.html'

    def get_queryset(self):
        return Company.objects.all()

class VenueCreate(CreateView):
    model = RehearsalVenues
    fields = ['name', 'location', 'company']
    template_name = 'create_form.html'

    def get_context_data(self, **kwargs):
        context = super(VenueCreate, self).get_context_data(**kwargs)
        context['companies'] = Company.objects.all()
        return context

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
        return Company.objects.all()

class UploadsCreate(CreateView):
    model = Uploads
    fields = ['name', 'file', 'details', 'company']
    template_name = 'create_form.html'

    def get_context_data(self, **kwargs):
        context = super(UploadsCreate, self).get_context_data(**kwargs)
        context['companies'] = Company.objects.all()
        return context

class UploadsUpdate(UpdateView):
    model = Uploads
    fields = ['name', 'file', 'details']
    template_name = 'create_form.html'

class UploadsDelete(DeleteView):
    model = Uploads
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('getdata:documents')

class AddPerformer(View):
    form_class = AddPerformerForm
    template_name = 'create_form.html'

    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    #register user based on input data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = self.request.user

            # unify the data into commit-ready format (cleaned data or normalized)
            email = form.cleaned_data['email']
            company = Company.objects.get(username=user.username)
            try:
                performer = Performers.objects.get(email=email)
            except:
                raise Http404("Email does not exist")
            company.performers.add(performer)
            company.save()
            return redirect('getdata:home')
        return render(request, self.template_name, {'form': form})

class PrivacyChange(generic.ListView):
    template_name = 'profile.html'

    def get_queryset(self):
        return Performers.objects.get(username=self.request.user.username)

    def post(self, request):
        performer = Performers.objects.get(username=request.user.username)
        if performer.public_profile == True:
            performer.public_profile = False
        else:
            performer.public_profile = True
        performer.save()
        return redirect('getdata:profile')
