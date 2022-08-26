from pycoin.symbols.bch import network
import requests
import getpass
import json
import io
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
sec_key = "L5h6rJHPVrWs1LLwgLM22kcBtQq2KzvXccAS52ytzVdD3JMMTSKp"
source_tx = "928d81954a4b1fb87af444bc657e5f939a333f13a5233b23b1af73d0ba23077d"
tx = Tx.from_hex(source_tx)
spendable = tx.tx_outs_as_spendable()[1]
new_tx = create_tx([spendable],[(dest_address, 100000000), source_tx])
new_tx_hex = new_tx.as_hex()
print(new_tx_hex)


from bitcoinrpc.authproxy import AuthServiceProxy
conn = AuthServiceProxy("http://%s:%s@192.168.1.103:18332"%("fftest","fftest123"))
print(conn.decoderawtransaction(new_tx_hex))
