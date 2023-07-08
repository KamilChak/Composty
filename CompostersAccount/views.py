
from decimal import Decimal
import json
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from Blockchain.views import Blockchain
from .forms import ComposterForm, ComposterLoginForm
from .models import Composter
from GreenersAccount.models import Greener, Offer, GreenerNotifications
from django.contrib import messages
#libraries for auth
from django.contrib.auth.hashers import make_password
from .backends import ComposterAuthBackend
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Sum,Min,Max
from django.views.decorators.csrf import csrf_exempt



def composterSignup(request):
    if request.method == 'POST':
        form = ComposterForm(request.POST)
        if form.is_valid():

            organization_name = form.cleaned_data['OrganizationName']
            community_name = form.cleaned_data['CommunityName']
            email = form.cleaned_data['Email']
            password = make_password(form.cleaned_data['password'])
            phone_number = form.cleaned_data['PhoneNumber']
            location = form.cleaned_data['Location']
            
            composter = Composter.objects.create(OrganizationName=organization_name, CommunityName=community_name, Email=email, password=password, PhoneNumber=phone_number, Location=location)

            blockchain = Blockchain()

            user_url = request.build_absolute_uri('/')[:-1]
            blockchain.add_node(user_url, composter)
            
            return redirect('/')
    else:
        form = ComposterForm()

    return render(request, 'Composter_signup.html', {'form': form})



def composterLogin(request):
    if request.method == 'POST':
        form = ComposterLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(request=request, email=email, password=password, backend=ComposterAuthBackend())

            if user is not None:
                if isinstance(user, Greener):
                    messages.error(request, 'Invalid email or password.')
                else:
                    login(request, user)
                    return redirect('composterHome')
            else:
                messages.error(request, 'Invalid email or password.')

        remember_me = request.POST.get('remember')

        if remember_me:
            request.session.set_expiry(604800)
        else:
            request.session.set_expiry(0)

    else:
        form = ComposterLoginForm()

    return render(request, 'Composter_login.html', {'form': form})



@login_required
def composterHome(request):
    if request.user.is_authenticated:
        composter = request.user
        latitude = composter.Location.y
        longitude = composter.Location.x

        greeners = composter.composters.all()

        context = {
            'composter': composter,
            'latitude': latitude,
            'longitude': longitude,
            'greeners': greeners,
        }
        return render(request, 'Composter_home.html', context)

    else:
        return redirect('composterHome')



@login_required
def composterGreenersRequest(request):
    offers = Offer.objects.filter(sender__composter=request.user).order_by('-id')
    
    context = {
        'offers': offers
    }
    return render(request, 'greeners_request.html', context)



@login_required
def confirm_offer(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    
    blockchain = Blockchain()

    amount = Decimal(str(offer.green_material + offer.brown_material + offer.manure))
    #add_transation(sender, recipient, amount, time)
    transaction = blockchain.add_transaction(request.user, offer.sender, amount, timezone.now())

    blockchain.mine_block(transaction)

    offer.sender.wallet += amount
    offer.sender.save()

    offer.Status = 'completed'
    offer.save()

    notification_message = request.user.CommunityName + " has accepted your offer! You gained " + str(amount) + " Compo Coins!"
    GreenerNotifications.objects.create(greener=offer.sender, Message=notification_message)

    return redirect('composterGreenersRequest')



@login_required
def decline_offer(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)

    offer.Status = 'declined'
    offer.save()

    notification_message = "Unfortunatly, " + request.user.CommunityName + " has declined your offer"
    GreenerNotifications.objects.create(greener=offer.sender, Message=notification_message)

    return redirect('composterGreenersRequest')



@login_required
def GreenersOffers(request):
    offers = Offer.objects.filter(sender__composter=request.user, Status='pending').select_related('sender').values('sender_id', 'sender__FirstName', 'sender__LastName', 'sender__Location').annotate(
        manure=Sum('manure'),
        green_material=Sum('green_material'),
        brown_material=Sum('brown_material'),
        date_range_start=Max('date_range_start'),
        date_range_end=Min('date_range_end')
    ).order_by('sender_id')

    GreenersOffersJson = []
    for offer in offers:
        GreenersOffersJson.append({
            'GreenerId': offer['sender_id'],  
            'GreenerFirstName' : offer['sender__FirstName'],
            'GreenerLastName': offer['sender__LastName'],
            'GreenerLocationX': offer['sender__Location'].x,
            'GreenerLocationY': offer['sender__Location'].y,
            'manure': offer['manure'],
            'green_material': offer['green_material'],
            'brown_material': offer['brown_material'],
            'date_range_start': offer['date_range_start'],
            'date_range_end': offer['date_range_end']
        }) 
    return JsonResponse({'GreenersOffersJson': GreenersOffersJson})



@login_required
def getPendingMembers(request):
    greeners = Greener.objects.filter(composter=request.user, ComposterStatus='waiting')
    context = {'greenersArray': greeners}
    return render(request, 'pending_members.html', context)



@csrf_exempt
@login_required
def acceptGreener(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        greener_id = data.get('greenerId')
        if greener_id is not None:
            greener = Greener.objects.get(id=greener_id, composter__id=request.user.id, ComposterStatus='waiting')
            greener.ComposterStatus = 'accepted'
            greener.save()

            notification_message = "Congratulations! You have been accepted to "+ request.user.CommunityName +"community."
            GreenerNotifications.objects.create(greener=greener, Message=notification_message)

            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})



@csrf_exempt
@login_required
def rejectGreener(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        greener_id = data.get('greenerId')
        if greener_id is not None:
            greener = Greener.objects.get(id=greener_id, composter__id=request.user.id, ComposterStatus='waiting')
            greener.composter = None
            greener.save()

            notification_message = "Unfortunately, your request to Community: " + request.user.CommunityName + " has been rejected !"
            GreenerNotifications.objects.create(greener=greener, Message=notification_message)
            
            return JsonResponse({'status':'ok'})
    return JsonResponse({'status': 'error'})



@login_required
def getGreenersOffer(request):
    offers = Offer.objects.filter(Greener__composter=request.user)
    offersArray = []
    for offer in offers:
        offersArray.append({
            'offerid' : offer.id,
            'Greener': offer.sender,
            'manure': offer.manure,
            'brown_material': offer.brown_material,
            'green_material': offer.green_material,
            'date_range_start': offer.date_range_start,
            'date_range_end': offer.date_range_end,
            'Status': offer.Status
        }) 
    return render(request , 'greeners_request.html',{'offersArray': offersArray})



@login_required
def getComposterMembers(request):
    members = Greener.objects.filter(composter = request.user, ComposterStatus='accepted')
    context = {'membersArray' : members}
    return render(request, 'Composter_members.html', context)


@login_required
def removeComposterMember(request, member_id):
    member = get_object_or_404(Greener, pk=member_id)
    member.composter = None
    member.ComposterStatus = 'waiting'
    member.save()

    notification_message = "Unfortunately, you were kicked out from the community: " + request.user.CommunityName
    GreenerNotifications.objects.create(greener=member, Message=notification_message)
    
    return redirect('getComposterMembers')


def logoff(request):
    logout(request)
    return redirect('index')


def checkEmail(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        print(email)

        exists = Composter.objects.filter(Email=email).exists() or Greener.objects.filter(Email=email).exists()
        print(exists)

        return JsonResponse({'exists': exists})