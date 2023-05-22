from django.shortcuts import render
from django.urls import reverse_lazy
from Blockchain.models import Transaction
from django.db.models import Sum
from CompostersAccount.models import Composter
from GreenersAccount.models import Greener, Offer

from .decorators import superuser_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView




class AdminLoginView(LoginView):
    template_name = 'admin/login.html'
    redirect_authenticated_user = True


class AdminLogoutView(LogoutView):
    next_page = reverse_lazy('adminUI:login')




@login_required
@superuser_required
def adminUI(request):
    transactions = Transaction.objects.all()
    
    compostersT = Composter.objects.count()
    greenersT = Greener.objects.count()
    transactionsT = Transaction.objects.count()
    offersT = Offer.objects.count()

    today = datetime.today()
    #transactions filtered by date
    today_transactions = Transaction.objects.filter(timestamp__date=today)

    month_transactions = Transaction.objects.filter(timestamp__month=today.month)

    year_transactions = Transaction.objects.filter(timestamp__year=today.year)

    #transactions sums by date    
    daily_total = today_transactions.aggregate(Sum('amount'))['amount__sum'] or 0

    monthly_total = month_transactions.aggregate(Sum('amount'))['amount__sum'] or 0

    yearly_total = year_transactions.aggregate(Sum('amount'))['amount__sum'] or 0

    
    context = {
        'transactions': transactions,
        'daily_total': daily_total,
        'monthly_total': monthly_total,
        'yearly_total': yearly_total,
        'transactionsT': transactionsT,
        'offersT': offersT,
        'compostersT': compostersT,
        'greenersT': greenersT,
    }
    return render(request, 'adminUI.html', context)


def google_maps(request):
  context = {
    'parent': 'maps',
    'segment': 'google_maps'
  }
  return render(request, 'pages/map-google.html', context)