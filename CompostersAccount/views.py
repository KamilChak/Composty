from django.shortcuts import render, redirect
from .forms import ComposterForm, ComposterLoginForm
from .models import Composter
from GreenersAccount.models import Greener
from django.contrib import messages

#libraries for auth
from django.contrib.auth.hashers import make_password
from .backends import ComposterAuthBackend
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def composterSignup(request):
    if request.method == 'POST':
        form = ComposterForm(request.POST)
        if form.is_valid():
            # do something with the cleaned form data
            organization_name = form.cleaned_data['OrganizationName']
            community_name = form.cleaned_data['CommunityName']
            email = form.cleaned_data['Email']
            password = make_password(form.cleaned_data['password'])
            phone_number = form.cleaned_data['PhoneNumber']
            location = form.cleaned_data['Location']
            
            # create a new Composter object with the cleaned form data
            composter = Composter.objects.create(OrganizationName=organization_name, CommunityName=community_name, Email=email, password=password, PhoneNumber=phone_number, Location=location)
            composter.save()
            
            # redirect to the success page
            return redirect('/')  # or any other success page
    else:
        form = ComposterForm()

    return render(request, 'Composter_signup.html', {'form': form})


def composterLogin(request):
    if request.method == 'POST':
        form = ComposterLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Authenticate the user using my custom backend
            user = authenticate(request=request, email=email, password=password, backend=ComposterAuthBackend())

            if user is not None:
                if isinstance(user, Greener):
                    # Reject the login attempt if the user is a Greener
                    messages.error(request, 'Invalid email or password.')
                else:
                    # Authenticate the user and redirect to the home page
                    login(request, user)
                    return redirect('composterHome')
            else:
                # Authentication failed, show an error message
                messages.error(request, 'Invalid email or password.')
    else:
        form = ComposterLoginForm()

    return render(request, 'Composter_login.html', {'form': form})


@login_required
def composterHome(request):
    return render(request, 'Composter_home.html')

@login_required
def composterCalendar(request):
    return render(request, 'composter_calendar.html')

@login_required
def composterGreenersRequest(request):
    return render(request, 'greeners_request.html')

def logoff(request):
    logout(request)
    return redirect('index')