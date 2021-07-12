import json
from web3 import Web3
from web3.providers.rpc import HTTPProvider
from web3.middleware import geth_poa_middleware
from eth_utils import address, to_checksum_address, encode_hex
import requests

merkle_drop_abi = json.load(
    open("../build/contracts/MerkleDrop.json"))["abi"]


def claim(web3, contract_address, amount, proof, address, privkey):

    merkle_drop_contract = web3.eth.contract(
        address=contract_address, abi=merkle_drop_abi
    )

    tx = merkle_drop_contract.functions.claim(amount, proof).buildTransaction({
        'from': address,
        'value': 0,
        'gasPrice': web3.toWei(10, 'gwei'),
        'gas': 1500000,
        "nonce": w3.eth.getTransactionCount(address),
    })

    signed_tx = web3.eth.account.sign_transaction(tx, private_key=privkey)
    txhash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    receipt = web3.eth.waitForTransactionReceipt(txhash, timeout=15)
    print('receipt', receipt)


def isClaimed(web3, contract_address, address):
    merkle_drop_contract = web3.eth.contract(
        address=contract_address, abi=merkle_drop_abi
    )
    return merkle_drop_contract.functions.isClaimed(address).call()


if __name__ == "__main__":
    http_addr = "https://kovan.infura.io/v3/"
    contract_address = ''
    w3 = Web3(HTTPProvider(http_addr, request_kwargs={'timeout': 6000}))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    address = ''
    privkey = ''

    ret = requests.get(f'http://127.0.0.1:5000/merkle_proof/{address}')
    data = ret.json()

    is_claimed = isClaimed(w3, contract_address, address)

    if not is_claimed:
        claim(w3, contract_address,
              data['tokenURI'], data['proof'], address, privkey)
        pass
    else:
        print("claimed")
