from django.http import Http404, HttpResponse
from django.shortcuts import render
import requests
import json
from pycoin.solve.utils import build_hash160_lookup
from pycoin.ecdsa.secp256k1 import secp256k1_generator
from .models import Transaction
from . import create_transaction

def index(request):
    transaction_list = Transaction.objects.all()
    return render(request, 'transact/list.html', {'transaction_list': transaction_list})

def detail(request, transaction_id):
    try:
        t = Transaction.objects.get( id = transaction_id)
    except:
        raise Http404("Транзакци не найдена!")

    return render(request, 'transact/detail.html', {'transaction': t})

def transaction_send(request):
    url = "http://45.32.232.25:3669/wallet/testwallet"
    rpc_user = 'bcs_tester'
    rpc_password = 'iLoveBCS'
    payload = json.dumps({"method": "getnewaddress", "params": []})
    headers = {'content-type': "application/json", 'cache-control': "no-cache"}
    response = requests.request("POST", url, data=payload, headers=headers, auth=(rpc_user, rpc_password))
    address = json.loads(response.text)['result']

    tx_sum = 1000000
    tx = create_transaction.New_tx(address)

    signed_tx, signed_hex = tx.create_tx(satoshi_value=tx_sum, solver_f=build_hash160_lookup, generator=secp256k1_generator)
    print(signed_tx)
    print(signed_hex)
    payload = json.dumps({"method": "sendrawtransaction", "params": [signed_hex]})
    response = requests.request("POST", url, data=payload, headers=headers, auth=(rpc_user, rpc_password))

    tx_to_db = Transaction(transaction_id = json.loads(response.text)['txid'], transaction_sum = tx_sum, transaction_description = "")
    tx_to_db.save()

    return index(request)