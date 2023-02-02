from django.shortcuts import render, get_object_or_404, redirect
from .forms import NameForm, UserForm, AddPerformerForm, AddStaffForm
from .models import Performers, Shows, Roles, CallTime, RehearsalVenues, Uploads, Company, Staff
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.http import Http404
from django.core.mail import EmailMessage
from getdata.utils import render_to_pdf
from django.http import HttpResponse
import os
import requests
from django import forms

all_performers = Performers.objects.all()
all_shows = Shows.objects.all()
all_roles = Roles.objects.all()

# for use with pythonanywhere.com
# schedulename = 0

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
    fields = [ 'email']
    template_name = 'create_form.html'

    def get_form(self, *args, **kwargs):
        form = super(CompanyUpdate, self).get_form(*args, **kwargs)
        c = Company.objects.get(username=self.request.user.username)

        return form

class CompanyPerformersUpdate(UpdateView):
    model = Company
    fields = [ 'performers']
    template_name = 'create_form.html'

    def get_form(self, *args, **kwargs):
        form = super(CompanyPerformersUpdate, self).get_form(*args, **kwargs)
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
        form.fields['rehearsal_start'].widget = forms.DateInput(attrs={'type':'date'})
        form.fields['show_open'].widget = forms.DateInput(attrs={'type':'date'})
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
        if self.request.user.groups.all().last == "Company":
            company = Company.objects.filter(username=self.request.user.username)
        else:
            company = Company.objects.all()
        return company

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
        form.fields['rehearsal_start'].widget = forms.DateInput(attrs={'type':'date'})
        form.fields['show_open'].widget = forms.DateInput(attrs={'type':'date'})
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
        form.fields['date'].widget = forms.DateInput(attrs={'type':'date'})
        form.fields['start_time'].widget = forms.TimeInput(attrs={'type':'time'})
        form.fields['end_time'].widget = forms.TimeInput(attrs={'type':'time'})
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


class CreatePDF(View):

    def post(self, request, *args, **kwargs):
        text = request.POST.get("schedule")
        data = {
             'id': 4,
        }
        # the path for pythonanywhere.com MUST BE '/home/dylanelza/theater/getdata/templates/schedule ... etc.'
        file = open("C:/Users/dylan/OneDrive/Documents/GitHub/Portfolio/Backend Projects/theater-django/theater/getdata/templates/schedule.html", "w")
        file.seek(0)
        file.write(text)
        file.close()
        pdf = render_to_pdf('schedule.html', data)
        user = Company.objects.get(username=request.user.username)
        list = []
        bcclist = []
        for performer in user.performers.all():
            list.append(performer.email)

        for staff in user.staff_set.all():
            bcclist.append(staff.email)

        mail = EmailMessage(
            f"New Daily Schedule from {user.name}",
            "Here is today's schedule!",
            user.email,
            list,
            bcclist,
            reply_to=[user.email]
        )
        mail.attach('DailySchedule.pdf', bytes(pdf), "application/pdf")
        mail.send()
        return HttpResponse(pdf, content_type='application/pdf')

    # the following is for use on pythonanywhere.com - uses an auto reload feature to fix major bug with schedule pdfs
    """ class CreatePDF(View):

    def post(self, request, *args, **kwargs):
        global schedulename

        user = Company.objects.get(username=request.user.username)
        text = request.POST.get("schedule")
        current_show = request.POST.get("showtitle")
        current_date = request.POST.get("date")
        text = f'<h1 style="text-align: center;">{user.name}</h1>' + text
        file = open("/home/dylanelza/theater/getdata/templates/schedule" + str(schedulename) + ".html", "w")
        file.write(text)
        file.close()
        data = {}
        pdf = render_to_pdf(file.name, data)
        schedulename += 1
        list = []
        bcclist = []

        for performer in user.performers.all():
            for role in performer.roles_set.all():
                if role.show_id.title == current_show:
                    list.append(performer.email)

        for staff in user.staff_set.all():
            bcclist.append(staff.email)

        mail = EmailMessage(
            f"{current_show} {current_date} Daily Schedule - {user.name}",
            f"Here is the schedule for {current_date}. View it online at: dylanelza.pythonanywhere.com/getdata/home",
            user.email,
            list,
            bcclist,
            reply_to=[user.email],
        )

        mail.attach('DailySchedule.pdf', bytes(pdf), "application/pdf")

        if schedulename >= 10:
            for x in range(schedulename):
                os.remove("/home/dylanelza/theater/getdata/templates/schedule" + str(x) + ".html")

            schedulename = 0
            username = "dylanelza"
            api_token = "aff4d5c66d1091bb59d297a1d6fc6815ebd98584"
            domain_name = "dylanelza.pythonanywhere.com"

            response = requests.post(
                'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain_name}/reload/'.format(
                    username=username, domain_name=domain_name
                ),
                headers={'Authorization': 'Token {token}'.format(token=api_token)}
            )
            if response.status_code == 200:
                print('reloaded OK')
            else:
                print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))

        mail.send()
        return HttpResponse(pdf, content_type='application/pdf') """

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
        form.fields['date'].widget = forms.DateInput(attrs={'type':'date'})
        form.fields['start_time'].widget = forms.TimeInput(attrs={'type':'time'})
        form.fields['end_time'].widget = forms.TimeInput(attrs={'type':'time'})
        return form

class CallDelete(DeleteView):
    model = CallTime
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('getdata:home')

class VenueView(generic.ListView):
    template_name = 'venues.html'

    def get_queryset(self):
        if self.request.user.groups.all().last == "Company":
            company = Company.objects.filter(username=self.request.user.username)
        else:
            company = Company.objects.all()
        return company

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
        if self.request.user.groups.all().last == "Company":
            company = Company.objects.filter(username=self.request.user.username)
        else:
            company = Company.objects.all()
        return company

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

class AddStaff(View):
    form_class = AddStaffForm
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
            name = form.cleaned_data['name']
            company = Company.objects.get(username=user.username)
            staff = Staff()
            staff.name = name
            staff.email = email
            staff.company = company
            staff.save()
            return redirect('getdata:staffinfo')
        return render(request, self.template_name, {'form': form})

class StaffView(generic.ListView):
    template_name = 'staff.html'

    def get_queryset(self):
        company = Company.objects.get(username=self.request.user.username)
        return Staff.objects.filter(company=company)

class StaffUpdate(UpdateView):
    model = Staff
    fields = ['name', 'email']
    template_name = 'create_form.html'

class StaffDelete(DeleteView):
    model = Staff
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('getdata:staffinfo')

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

class SendAlert(generic.ListView):
    template_name = 'profile.html'

    def post(self, request):
        user = Company.objects.get(username=request.user.username)
        list = []
        bcclist = []
        for performer in user.performers.all():
            list.append(performer.email)
        
        for staff in user.staff_set.all():
            bcclist.append(staff.email)

        mail = EmailMessage(
            f"Call Time Alert from {user.name}",
            request.POST.get('alert'),
            user.email,
            list,
            bcclist,
            reply_to=[user.email],
        )
        mail.send()
        return redirect('getdata:profile')