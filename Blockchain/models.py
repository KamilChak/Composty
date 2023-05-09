from django.db import models
from django.utils import timezone

from GreenersAccount.models import Greener, Composter


class Transaction(models.Model):
    sender = models.ForeignKey(Composter, on_delete=models.CASCADE, related_name='sent_transactions')
    recipient = models.ForeignKey(Greener, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)
    
class Node(models.Model):
    address = models.CharField(max_length=200)
    user_id = models.IntegerField()

class Block(models.Model):
    index = models.IntegerField()
    previous_hash = models.CharField(max_length=100)
    hash = models.CharField(max_length=100)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True, blank=True)
    nonce = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)