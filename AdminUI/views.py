from django.shortcuts import render
from Blockchain.models import Transaction
from django.db.models import Sum

from .decorators import superuser_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from datetime import datetime


class AdminLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


@login_required
@superuser_required
def adminUI(request):
    transactions = Transaction.objects.all()

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
    }
    return render(request, 'adminUI.html', context)
