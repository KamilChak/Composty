import datetime
import hashlib
import json
from urllib.parse import urlparse
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Block, Node, Transaction
from django.db.utils import ProgrammingError


# Huge thanks to 'Mohammed Gumma' for providing the basic blockchain layout
# https://medium.com/@MKGOfficial/build-a-simple-blockchain-cryptocurrency-with-python-django-web-framework-reactjs-f1aebd50b6c

class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        self.load_nodes()
        self.load_blocks()

    def load_blocks(self):
        try:
            self.chain = Block.objects.all().order_by('index')
        except ProgrammingError:
            self.chain = []
    
    def add_node(self, address, user):
        parsed_url = urlparse(address)
        node = Node(address=parsed_url.netloc, user_id=user.id)
        node.save()

    def load_nodes(self):
        try:
            for node in Node.objects.all():
                self.nodes.add((node.address, node.user_id))
        except ProgrammingError:
            self.nodes = set()

    def add_transaction(self, sender, recipient, amount, time):
        transaction = Transaction.objects.create(
            sender=sender,
            recipient=recipient,
            amount=amount,
            timestamp=time
        )
        transaction.save()
        self.current_transactions.append(transaction)
        return transaction



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

    def mine_block(self, transaction):
        previous_block = Block.objects.last()
        previous_hash = previous_block.hash
        nonce = self.proof_of_work(previous_hash)

        block_hash = self.hash({
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'nonce': nonce,
            'transaction': {
                'sender': transaction.sender.id,
                'recipient': transaction.recipient.id,
                'amount': str(transaction.amount),
                'time': str(transaction.timestamp)
            },
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


def display_chain(request):
    try:
        chain = Block.objects.all()
        if chain:
            context = {'chain': chain}
            return render(request, 'chain.html', context)
        else:
            return JsonResponse({'message': 'No blocks found.'}, status=200)
    except Exception as e:
        error_message = str(e)
        return JsonResponse({'error': error_message}, status=500)


@csrf_exempt
def display_nodes(request):
    
    nodes = Node.objects.all()
    context = {
        'nodes': nodes,
    }
    
    return render(request, 'display_nodes.html', context)
