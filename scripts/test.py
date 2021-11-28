from web3 import Web3
from web3.middleware import geth_poa_middleware
import json
import os

#web3 = Web3(Web3.HTTPProvider('https://speedy-nodes-nyc.moralis.io/09dd853d231566671a467e96/polygon/mainnet'))
#web3.middleware_onion.inject(geth_poa_middleware, layer=0)
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

key = '0x1b50c6f8541bfa542e9a39a5dae489e7585600d929610087a068cda41a827b05' # os.environ['ETHEREUM_PRIVATE_KEY']
#me = "0xc4192029059E1D3a522751cCFc3E2Bf7f3c1172e"
me = '0x52f0e1D0a6dc86B84c09BD8Dde83E3EEAB2d96A1'

abi = open("./build/SwearJar.abi", "r").read()

jar = web3.eth.contract(address=web3.toChecksumAddress("0x8fa8c9e14c7b4b4b87bd27a85adfe1a7bc341b51"), abi=abi)

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

