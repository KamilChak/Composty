from django.shortcuts import render, redirect
from .forms import GreenerForm, GreenerLoginForm
from .models import Greener
from CompostersAccount.models import Composter
from django.http import JsonResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from CompostersAccount.models import Composter
from django.contrib.gis.geos import GEOSGeometry
from CompostItem.models import Compost

#libraries for auth
from django.contrib.auth.hashers import make_password
from .backends import GreenerAuthBackend
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


# Create your views here.

def greenerSignup(request):
    if request.method == 'POST':
        form = GreenerForm(request.POST)
        if form.is_valid():
            # do something with the cleaned form data
            first_name = form.cleaned_data['FirstName']
            last_name = form.cleaned_data['LastName']
            email = form.cleaned_data['Email']
            password = make_password(form.cleaned_data['password'])
            phone_number = form.cleaned_data['PhoneNumber']
            location = form.cleaned_data['Location']
            composterObject = form.cleaned_data['composter']           
             
            # create a new Greener object with the cleaned form data
            greener = Greener.objects.create(FirstName=first_name, LastName=last_name, Email=email, password=password, PhoneNumber=phone_number, Location = location, composter = composterObject)
            greener.save()
            # redirect to the success page
            return redirect('/')  # or any other success page
    else:
        form = GreenerForm()

    return render(request,'Greener_signup.html',{'form': form})

#----------------------------------------------------------------------#

def greenerLogin(request):
    if request.method == 'POST':
        form = GreenerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Authenticate the user using my custom backend
            user = authenticate(request=request, email=email, password=password, backend=GreenerAuthBackend())

            if user is not None:
                if isinstance(user, Composter):
                    # Reject the login attempt if the user is a Greener
                    messages.error(request, 'Invalid email or password.')
                else:
                    # Authenticate the user and redirect to the home page
                    login(request, user)
                    return redirect('greenerHome')
            else:
                # Authentication failed, show an error message
                messages.error(request, 'Invalid email or password.')
    else:
        form = GreenerLoginForm()

    return render(request, 'Greener_login.html', {'form': form} )

#-----------------------------------------------------------------------#


@login_required
def greenerHome(request):
    user = request.user
    context = {'user': user}
    return render(request, 'Greener_home.html', context)


#----------------------------API during signup for picking up the closest compster-------------------------------------------#


def getClosestComposters(request):
    UserLocationWKT = request.GET.get('UserLocation')
    UserLocationWKB = GEOSGeometry(UserLocationWKT)
    point = Point(UserLocationWKB.x,UserLocationWKB.y, srid=4326)
    
    

    composters = Composter.objects.filter(Location__distance_lte=(point, 10000)).annotate(distance=Distance('Location', point)).order_by('distance')

    closest_composters = []
    for composter in composters:
        closest_composters.append({
            'id': composter.id,
            'OrganizationName': composter.OrganizationName,
            'CommunityName': composter.CommunityName,
            'Email': composter.Email,
            'PhoneNumber': composter.PhoneNumber,
            'distance': composter.distance.m,
            'LocationX': str(composter.Location.x),
            'LocationY': str(composter.Location.y)
        })

    return JsonResponse({'closest_composters': closest_composters})



@login_required
def compostOffer(request):
    composts = Compost.objects.all()
    context = {'composts': composts}
    return render(request, 'Compost_offer.html', context)





def logoff(request):
    logout(request)
    return redirect('index')