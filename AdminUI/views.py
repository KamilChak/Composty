from django.shortcuts import render
from django.urls import reverse_lazy
from Blockchain.models import Transaction
from django.db.models import Sum
from CompostersAccount.models import Composter
from GreenersAccount.models import Greener, Offer

from .decorators import superuser_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
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

    date = datetime.today()
    #transactions filtered by date
    today_transactions = Transaction.objects.filter(timestamp__date=date)

    yesterday = date - timedelta(days=1)

    yesterday_transactions = Transaction.objects.filter(timestamp__date=yesterday)
    
    month_transactions = Transaction.objects.filter(timestamp__month=date.month)

    year_transactions = Transaction.objects.filter(timestamp__year=date.year)

    #last month t
    end_of_previous_month = date.replace(day=1) - timedelta(days=1)
    start_of_previous_month = end_of_previous_month.replace(day=1)

    last_month_transactions = Transaction.objects.filter(timestamp__date__range=[start_of_previous_month, end_of_previous_month])
    
    #last year t
    end_of_previous_year = date.replace(month=1, day=1) - timedelta(days=1)
    start_of_previous_year = end_of_previous_year.replace(month=1, day=1)

    last_year_transactions = Transaction.objects.filter(timestamp__date__range=[start_of_previous_year, end_of_previous_year])

    #transactions sums by date    
    daily_total = today_transactions.aggregate(Sum('amount'))['amount__sum'] or 0

    yesterday_total = yesterday_transactions.aggregate(Sum('amount'))['amount__sum'] or 0

    monthly_total = month_transactions.aggregate(Sum('amount'))['amount__sum'] or 0

    last_monthly_total = last_month_transactions.aggregate(Sum('amount'))['amount__sum'] or 0

    yearly_total = year_transactions.aggregate(Sum('amount'))['amount__sum'] or 0

    last_yearly_total = last_year_transactions.aggregate(Sum('amount'))['amount__sum'] or 0

    #calculate Percentages
    def calculateP(x,y):
        if (y == 0):
            if(x != 0):
                p = 100
            else:
                p = 0
        else:
            p = (x / y) * 100
        return "{:.2f}".format(p)
    

    today_yest_P = calculateP(daily_total, yesterday_total)
    last_month_this_month_P = calculateP(monthly_total, last_monthly_total)
    last_year_this_year_P = calculateP(yearly_total, last_yearly_total)

    context = {
        'transactions': transactions,
        'today_yest_P': today_yest_P,
        'last_month_this_month_P': last_month_this_month_P,
        'last_year_this_year_P': last_year_this_year_P,
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