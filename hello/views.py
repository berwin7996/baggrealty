from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .models import Tenant
from hello.forms import TenantForm
# Create your views here.
def index(request):
    return HttpResponse('Welcome to Bagg Realty!')


def db(request):

    tenant = Tenant()
    tenant.save()

    tenants = Tenant.objects.all()

    return render(request, 'db.html', {'tenants': tenant})

def get_tenant(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TenantForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TenantForm()

    return render(request, 'name.html', {'form': form})

def index(request):
    return HttpResponse('Welcome to Bagg Realty!')
