from pycoin.symbols.bch import network
import requests
import getpass
import json

import hashlib
import struct
import unittest

from pycoin.coins.exceptions import BadSpendableError

from pycoin.coins.Tx import Tx
from pycoin.coins.tx_utils import create_tx
from pycoin.encoding.hexbytes import b2h, b2h_rev, h2b
from pycoin.networks.bitcoinish import create_bitcoinish_network
network = create_bitcoinish_network(symbol="BCS", network_name="Blockchain Solutions",
subnet_name="mainnet", wif_prefix_hex="80", address_prefix_hex="19",
pay_to_script_prefix_hex="32", bip32_prv_prefix_hex="0488ade4",
bip32_pub_prefix_hex="0488B21E", bech32_hrp="bc", bip49_prv_prefix_hex="049d7878",
bip49_pub_prefix_hex="049D7CB2", bip84_prv_prefix_hex="04b2430c",
bip84_pub_prefix_hex="04B24746", magic_header_hex="F1CFA6D3", default_port=3666)

url = "http://45.32.232.25:3669/wallet/testwallet"
rpc_user = 'bcs_tester'
rpc_password = 'iLoveBCS'
payload = json.dumps({"method": "getnewaddress", "params": []})
headers = {'content-type': "application/json", 'cache-control': "no-cache"}
response = requests.request("POST", url, data=payload, headers=headers, auth=(rpc_user, rpc_password))
my_address = "BJ83xnqRkJZMSgGCNAUmmdPCairCSfEywi"
dest_address = json.loads(response.text)['result']

Spendable = network.tx.Spendable
Tx = network.tx
TxIn = network.tx.TxIn
TxOut = network.tx.TxOut

BITCOIN_ADDRESSES = [network.keys.private(i).address() for i in range(1, 21)]

WIFS = [network.keys.private(i).wif() for i in range(1, 21)]

FAKE_HASH = hashlib.sha256(struct.pack("Q", 1)).digest()
print(struct.pack("Q", 1))
print(FAKE_HASH)
sec_key = "L5h6rJHPVrWs1LLwgLM22kcBtQq2KzvXccAS52ytzVdD3JMMTSKp"
source_tx = "928d81954a4b1fb87af444bc657e5f939a333f13a5233b23b1af73d0ba23077d"

FEE = 10000

# create a fake Spendable
COIN_VALUE = 100000000
spendables = [Spendable(COIN_VALUE, network.contract.for_address(BITCOIN_ADDRESSES[0]), FAKE_HASH, 0)]

EXPECTED_IDS = [source_tx]

for count in range(1, 11):
    tx = network.tx_utils.create_signed_tx(spendables, BITCOIN_ADDRESSES[1:count+1], wifs=WIFS[:1])
    for idx in range(1, count+1):
        script = tx.txs_out[idx-1].puzzle_script()
        address = network.address.for_script(script)
    for i in range(count):
        extra = (1 if i < ((COIN_VALUE - FEE) % count) else 0)
tx = str(tx)[5:][:-1]

#payload = json.dumps({"method": "sendrawtransaction", "params": [tx]})
#response = requests.request("POST", url, data=payload, headers=headers, auth=(rpc_user, rpc_password))

# Spendable = network.tx.Spendable
# Tx = network.tx
# TxIn = network.tx.TxIn
# TxOut = network.tx.TxOut
#
# BITCOIN_ADDRESSES = [network.keys.private(i).address() for i in range(1, 21)]
#
# WIFS = [network.keys.private(i).wif() for i in range(1, 21)]
#
# FAKE_HASH = hashlib.sha256(struct.pack("Q", 1)).digest()
# print(struct.pack("Q", 1))
# print(FAKE_HASH)
# sec_key = "L5h6rJHPVrWs1LLwgLM22kcBtQq2KzvXccAS52ytzVdD3JMMTSKp"
# source_tx = "928d81954a4b1fb87af444bc657e5f939a333f13a5233b23b1af73d0ba23077d"
#
# FEE = 10000
#
# # create a fake Spendable
# COIN_VALUE = 100000000
# spendables = [Spendable(COIN_VALUE, network.contract.for_address(BITCOIN_ADDRESSES[0]), FAKE_HASH, 0)]
#
# EXPECTED_IDS = [source_tx]
#
# for count in range(1, 11):
#     tx = network.tx_utils.create_signed_tx(spendables, BITCOIN_ADDRESSES[1:count+1], wifs=WIFS[:1])
#     for idx in range(1, count+1):
#         script = tx.txs_out[idx-1].puzzle_script()
#         address = network.address.for_script(script)
#     for i in range(count):
#         extra = (1 if i < ((COIN_VALUE - FEE) % count) else 0)
# tx = str(tx)[5:][:-1]
#
# #payload = json.dumps({"method": "sendrawtransaction", "params": [tx]})
# #response = requests.request("POST", url, data=payload, headers=headers, auth=(rpc_user, rpc_password))
