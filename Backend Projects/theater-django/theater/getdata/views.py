from django.shortcuts import render, get_object_or_404
from .forms import NameForm
from .models import Performers, Shows, Roles


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
        name = form.name
        email = form.email
        phone = form.phone
        context = {
            'form': form,
            'name': name,
            'email': email,
            'phone': phone
        }
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
