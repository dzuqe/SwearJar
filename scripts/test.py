from web3 import Web3
from web3.middleware import geth_poa_middleware
import json
import os

#web3 = Web3(Web3.HTTPProvider('https://speedy-nodes-nyc.moralis.io/09dd853d231566671a467e96/polygon/mainnet'))
#web3.middleware_onion.inject(geth_poa_middleware, layer=0)
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

key = os.environ['ETH_KEY'] # os.environ['ETHEREUM_PRIVATE_KEY']
#me = "0xc4192029059E1D3a522751cCFc3E2Bf7f3c1172e"
me = os.environ["ETH_ACC"]

contract_abi = open("./build/SwearJar.abi", "r").read()
token_abi = open("/home/hydrogen/polygon/scarg-token/build/ScarredEntertainment.abi", "r").read()

jar = web3.eth.contract(address=web3.toChecksumAddress("0xf6f9c82e3c86a058e549a4c135df196011ce74cf"), abi=contract_abi)
token = web3.eth.contract(address=web3.toChecksumAddress("0xf34e9bd70c9686c3023e25b23e5a9ea49f1f4b02"), abi=token_abi)

#etx = disp.functions.disperseEther(addresses, amounts).buildTransaction({
#    'gas': 1000000,
#    'value': web3.toWei(20, 'ether'),
#    'gasPrice': web3.toWei(1, 'gwei'),
#    'nonce': web3.eth.getTransactionCount(me),
#    'chainId': web3.eth.chainId
#})
#
#stx = web3.eth.account.signTransaction(etx, private_key=os.environ['ETHEREUM_PRIVATE_KEY'])
#rtx = web3.eth.sendRawTransaction(setx.rawTransaction)
#print(rtx.hex())

