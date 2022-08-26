from django.http import Http404, HttpResponse
from django.shortcuts import render
import requests, json
import io
from pycoin.coins.Tx import Tx
from pycoin.encoding.hexbytes import b2h, b2h_rev, h2b
from pycoin.networks.bitcoinish import create_bitcoinish_network
network = create_bitcoinish_network(symbol="BCS", network_name="Blockchain Solutions",
subnet_name="mainnet", wif_prefix_hex="80", address_prefix_hex="19",
pay_to_script_prefix_hex="32", bip32_prv_prefix_hex="0488ade4",
bip32_pub_prefix_hex="0488B21E", bech32_hrp="bc", bip49_prv_prefix_hex="049d7878",
bip49_pub_prefix_hex="049D7CB2", bip84_prv_prefix_hex="04b2430c",
bip84_pub_prefix_hex="04B24746", magic_header_hex="F1CFA6D3", default_port=3666)

from.models import Transaction

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
    # тут должна быть вся магия
    url = "http://45.32.232.25:3669/wallet/testwallet"
    rpc_user = 'bcs_tester'
    rpc_password = 'iLoveBCS'
    payload = json.dumps({"method": "getnewaddress", "params": []})
    headers = {'content-type': "application/json", 'cache-control': "no-cache"}
    response = requests.request("POST", url, data=payload, headers=headers, auth=(rpc_user, rpc_password))
    address = json.loads(response.text)['result']

    return index(request)