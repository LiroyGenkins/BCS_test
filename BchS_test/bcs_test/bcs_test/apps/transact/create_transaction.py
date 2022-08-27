import requests
import json
from pycoin.coins.bitcoin.Tx import Spendable
from pycoin.coins.tx_utils import create_tx
from pycoin.encoding.hexbytes import h2b

from pycoin.networks.bitcoinish import create_bitcoinish_network

network = create_bitcoinish_network(symbol="BCS", network_name="Blockchain Solutions",
subnet_name="mainnet", wif_prefix_hex="80", address_prefix_hex="19",
pay_to_script_prefix_hex="32", bip32_prv_prefix_hex="0488ade4",
bip32_pub_prefix_hex="0488B21E", bech32_hrp="bc", bip49_prv_prefix_hex="049d7878",
bip49_pub_prefix_hex="049D7CB2", bip84_prv_prefix_hex="04b2430c",
bip84_pub_prefix_hex="04B24746", magic_header_hex="F1CFA6D3", default_port=3666)

class New_tx():
    def __init__(self, destination_addr):
        self.dest_addr = destination_addr
        self.my_addr = "BJ83xnqRkJZMSgGCNAUmmdPCairCSfEywi"
        self.secret_key = "L5h6rJHPVrWs1LLwgLM22kcBtQq2KzvXccAS52ytzVdD3JMMTSKp"

    def create_tx(self, satoshi_value, solver_f, generator):
        utxo = self.get_utxo(self)
        spendables = Spendable(coin_value=int(utxo['value']), script=h2b(utxo['scriptPubKey']), tx_hash=h2b(utxo['transactionId']), tx_out_index=int(utxo['outputIndex']))
        self.unsigned_tx = create_tx(network=network, spendables=[spendables], payables=[tuple([self.dest_addr, satoshi_value])])
        self.unsigned_tx_hex = self.unsigned_tx.as_hex()
        key_wif = network.parse.wif(self.secret_key)
        exponent = key_wif.secret_exponent()
        solver = solver_f([exponent], [generator])

        self.signed_new_tx = self.unsigned_tx.sign(solver)
        self.signed_new_tx_hex = self.signed_new_tx.as_hex()

        return self.signed_new_tx, self.signed_new_tx_hex

    @classmethod
    def get_utxo(cls, self):
        utxo = requests.get(f'https://bcschain.info/api/address/{self.my_addr}/utxo')
        utxo = json.loads(utxo.text)[0]
        return utxo

