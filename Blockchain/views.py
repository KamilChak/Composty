import datetime
from decimal import Decimal
import hashlib
import json
from urllib.parse import urlparse
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from CompostersAccount.models import Composter
from GreenersAccount.models import Greener
from .models import Block, Node, Transaction


class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        self.load_nodes()
        self.load_blocks()

    def load_blocks(self):
        self.chain = Block.objects.all().order_by('index')
    
    def add_node(self, address, user):
        parsed_url = urlparse(address)
        node = Node(address=parsed_url.netloc, user_id=user.id)
        node.save()

    def load_nodes(self):
        for node in Node.objects.all():
            self.nodes.add((node.address, node.user_id))

    def add_transaction(self, sender, recipient, amount, time):
        
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'time': time
        })

        transaction = Transaction.objects.create(
            sender=sender,
            recipient=recipient,
            amount=amount
        )
        transaction.save()

    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True, cls=DjangoJSONEncoder).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, previous_hash):
        nonce = 0
        while True:
            hash_result = hashlib.sha256(f"{previous_hash}{nonce}".encode()).hexdigest()
            if hash_result[:4] == "0000":
                return nonce
            nonce += 1

    def mine_block(self):
        previous_block = Block.objects.last()
        previous_hash = previous_block.hash
        nonce = self.proof_of_work(previous_hash)

        transaction_dict = self.current_transactions[0]
        transaction = Transaction.objects.create(
            sender=transaction_dict['sender'],
            recipient=transaction_dict['recipient'],
            amount=transaction_dict['amount'],
            timestamp=transaction_dict['time'],
        )

        block_hash = self.hash({
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'nonce': nonce,
            'transaction': transaction_dict,
            'previous_hash': previous_hash
        })

        block = Block.objects.create(
            index=len(self.chain) + 1,
            timestamp=str(datetime.datetime.now()),
            nonce=nonce,
            transaction=transaction,
            previous_hash=previous_hash,
            hash=block_hash
        )
    
        block.save()
        self.current_transactions = []
        chain = list(Block.objects.all())
        chain.append(block)
        return block
    





blockchain = Blockchain()


"""@csrf_exempt
def transaction(request):
    composter_id = request.POST['composter_id']
    greener_id = request.POST['greener_id']
    amount = Decimal(request.POST['amount'])
    composter = Composter.objects.get(id=composter_id)
    greener = Greener.objects.get(id=greener_id)
    blockchain.add_transaction(composter.id, greener.id, amount, time=str(datetime.datetime.now()))
    block = blockchain.mine_block()
    greener.wallet += amount
    greener.save()
    response = {
        'message': f'Transaction successful! {amount} credits added to greener wallet.',
        'block': block
    }
    return JsonResponse(response)"""



def display_chain(request):
    chain = Block.objects.all()
    context = {'chain': chain}
    return render(request, 'chain.html', context)



@csrf_exempt
def display_nodes(request):
    
    nodes = Node.objects.all()
    context = {
        'nodes': nodes,
    }
    
    return render(request, 'display_nodes.html', context)
