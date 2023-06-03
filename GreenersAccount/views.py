from django.shortcuts import render, redirect
import json
from Blockchain.models import Transaction
from Blockchain.views import Blockchain
from .forms import CompostOfferForm, GreenerForm, GreenerLoginForm
from .models import Greener, Offer, GreenerNotifications
from CompostersAccount.models import Composter
from django.http import JsonResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from CompostersAccount.models import Composter
from django.contrib.gis.geos import GEOSGeometry
from CompostItem.models import Compost
from django.views.decorators.csrf import csrf_exempt

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

            blockchain = Blockchain()

            user_url = request.build_absolute_uri('/')[:-1]
            blockchain.add_node(user_url, greener)
            
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
                    if request.user.ComposterStatus == 'waiting':
                        return redirect('greenerHomeChooseComposter')
                    else:
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
    transactions = Transaction.objects.filter(recipient=user)

    notif = GreenerNotifications.objects.filter(greener=user).count()

    context = {
            'user': user,
            'transactions': transactions,
            'notif': notif,
            }
    return render(request, 'Greener_home.html', context)


#----------------------------API during signup for picking up the closest compster-------------------------------------------#


def getClosestComposters(request):
    UserLocationWKT = request.GET.get('UserLocation')
    UserLocationWKB = GEOSGeometry(UserLocationWKT)
    point = Point(UserLocationWKB.x, UserLocationWKB.y, srid=4326)
    
    radius = request.GET.get('Radius', 10000)
    radius = float(radius)*1000
    composters = Composter.objects.filter(Location__distance_lte=(point, radius)).annotate(distance=Distance('Location', point)).order_by('distance')

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

    if request.method == 'POST':
        form = CompostOfferForm(request.POST)
        if form.is_valid():
            manure = form.cleaned_data['manure']
            brown_material = form.cleaned_data['brown_material']
            green_material = form.cleaned_data['green_material']
            start_date = form.cleaned_data['date_range'].split(' to ')[0]
            end_date = form.cleaned_data['date_range'].split(' to ')[1]
            offer = Offer(sender=request.user,manure=manure, brown_material=brown_material, green_material=green_material, date_range_start=start_date, date_range_end=end_date)
            offer.save()
            return redirect('greenerHome')
    else:
        form = CompostOfferForm()

    user = request.user

    notif = GreenerNotifications.objects.filter(greener=user).count()

    composts = Compost.objects.all()
    context = {'composts': composts,
               'form': form,
               'notif': notif,
               }
    return render(request, 'Compost_offer.html', context)



@login_required
def sentRequests(request):

    user = request.user
    offers = Offer.objects.filter(sender=user).order_by('-id')

    notif = GreenerNotifications.objects.filter(greener=user).count()

    context = {
        'offers': offers,
        'notif': notif,
    }
    return render(request, 'greeners_requests.html', context)



def logoff(request):
    logout(request)
    return redirect('index')



@login_required
def greenerHomeChooseComposter(request):
    if request.user.ComposterStatus == 'accepted':
        return redirect('greenerHome')
    else:
        return render(request, 'Greener_home_choose_composter.html')
    


@login_required
def greenerRequestComposterLink(request):
    context = {'user' : request.user}
    if request.user.ComposterStatus == 'accepted':
        return redirect('greenerHome')
    else:
        return render(request, 'Greener_request_composter_link.html', context)
    


@csrf_exempt
@login_required
def updateComposter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        greener_id = data.get('greenerId')
        composter_id = data.get('composterId')
        if composter_id is not None:
            composter = Composter.objects.get(id=composter_id)
            greener = Greener.objects.get(id=greener_id)
            greener.composter = composter
            greener.save()
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})


@login_required
def greenerNotification(request):
    notifications = GreenerNotifications.objects.filter(greener__id=request.user.id).order_by('-Timestamp')
    context = {'notificationsArray': notifications}

    return render(request, 'Greener_notification.html', context)


def checkEmail(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        print(email)

        # Check if email exists in the Greener table
        exists = Greener.objects.filter(Email=email).exists()
        print(exists)

        return JsonResponse({'exists': exists})