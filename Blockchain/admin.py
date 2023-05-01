from django.contrib import admin

from .models import Block, Transaction, Node

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'recipient', 'amount', 'timestamp')


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'address')

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('index', 'previous_hash','hash','transaction','nonce', 'timestamp')