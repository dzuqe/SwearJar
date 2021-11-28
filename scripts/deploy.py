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

bytecode = open("./build/SwearJar.bin", "r").read()
abi = open("./build/SwearJar.abi", "r").read()

jar = web3.eth.contract(abi=abi, bytecode=bytecode)

dtx = jar.constructor(me, web3.toChecksumAddress("0x85131a5ea3f4d2a75b264e56a96751d8d5f131dd")).buildTransaction({
    'gas': 2000000,
    'gasPrice': web3.toWei(50, 'gwei'),
    'nonce': web3.eth.getTransactionCount(me),
    'chainId': web3.eth.chainId
})

stx = web3.eth.account.signTransaction(dtx, private_key=key)
ret = web3.eth.sendRawTransaction(stx.rawTransaction)

print("result: ", ret.hex())
