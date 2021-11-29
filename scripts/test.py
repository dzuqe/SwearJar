from web3 import Web3
from web3.middleware import geth_poa_middleware
import json
import os
import random
import sys

#web3 = Web3(Web3.HTTPProvider('https://speedy-nodes-nyc.moralis.io/09dd853d231566671a467e96/polygon/mainnet'))
#web3.middleware_onion.inject(geth_poa_middleware, layer=0)
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

key = os.environ['ETH_KEY'] # os.environ['ETHEREUM_PRIVATE_KEY']
#me = "0xc4192029059E1D3a522751cCFc3E2Bf7f3c1172e"
me = os.environ["ETH_ACC"]

eth = web3.eth

contract_abi = open("./build/SwearJar.abi", "r").read()
token_abi = open("/home/hydrogen/polygon/scarg-token/build/ScarredEntertainment.abi", "r").read()

jar_address = web3.toChecksumAddress("0xbbde180847bf3b9f87c8fbfaac301390f5205928")
token_address = web3.toChecksumAddress("0xb11c1cfcee8d5879fcc1c191719b9371b195bd38")

jar = eth.contract(address=jar_address, abi=contract_abi)
token = eth.contract(address=web3.toChecksumAddress(token_address), abi=token_abi)

users = [
    "0x191fa68Dc33C244ec7Dc7a07B43eEb7c7e67E5Fd",
    "0x86F2d2194b357EA24ecb1D5F60DAC79b5948a67d",
    "0x4149BEb99c96771b2fd7C1Af8d87FEA43Ee65FFA",
    "0x4e67ED4F4761303Af5189068F09510AEdFbc0dF5",
    "0xbFbaAFb3090Cc7F218C52695b1836970722e717E",
    "0xa150528A01035E9C60257CB7841015d754146128",
    "0x9B7123689E3C7a3394243090F853f0bD9f6CbEAE",
    "0x8CA4ba9061143588e4f7755163F6eb00165Fd920",
    "0x6585c5302C3C2fA836f9231EdA3b251A00c96E99",
    "0xe291DB7E182e324398Cc421D6084065d82D4651A",
]

keys = [
    "0x8585644ba3c6a61f72f88dd3f7a4bdc6bbdd94f8833591d7c723a5a44c008bed",
    "0x8f3ccd84b331c2f4c636edcea8889151b53dc3562184303ed9c4db56ff1418ff",
    "0x199a33b80942315005dcef7d74360d5fc8ca655c74dae8a134ea52d8a2fed8dc",
    "0x9e17ac0aaee1ca6e46435a3aefa9b818393fc2c362a0fa59f93fe713e5e87aec",
    "0x9e3dd88021c1c9f55560375a36260604f576938d57a704f986be42b44b402fff",
    "0x178be4aba5d0555ec55c7b58a11548baa3f53c1064f4ae8ac236d6f7bfdf7be9",
    "0x7ad6130f1ac851bbe88776656656e812259ffa15e1716b0b631b9f152d93c7c7",
    "0x6c43a5e6215977ca82b4c77f149703eb49e30a44a8271c064f2a92d4ca7d5e73",
    "0x8ab922dcf8d69724aed8bbafe07adba0f993d201df9c719cbc7803aaf496a96f",
    "0x839fc3b9338e78a3525d2760dd9863f38570dfc5f8c9ecdb27902358aa79a8cd",
]

words = ["fk", "sht", "motherfck", "horsesht", "fckwit", "goddam", "cant", "btch"]

tx_info = {
    'gas': 1000000,
    'gasPrice': web3.toWei(1, 'gwei'),
    'chainId': eth.chainId,
    'from': '',
    'nonce': '',
}

# utils
def sos(tx, _key):
   signed = eth.account.signTransaction(tx, private_key=_key)
   result = eth.sendRawTransaction(signed.rawTransaction)
   print(result.hex())


print("approve me")
tx_info.update({'nonce': eth.getTransactionCount(me)})
tx_info.update({'from': me})
amount = web3.toWei(10000000, 'ether')
me_approve_tx = token.functions.approve(jar_address, amount).buildTransaction(tx_info)
sos(me_approve_tx, key)

print("approve for everyone else")
for id in range(1, len(users)):
    tx_info.update({'nonce': eth.getTransactionCount(users[id])})
    tx_info.update({'from': users[id]})
    amount = web3.toWei(1000000, 'ether')
    approve_tx = token.functions.approve(jar_address, amount).buildTransaction(tx_info)
    sos(approve_tx, keys[id])

print("send users erc20")
for id in range(1, len(users)):
   tx_info.update({'nonce': eth.getTransactionCount(me)})
   tx_info.update({'from': me})
   transfer_tx = token.functions.transfer(users[id], web3.toWei(300000, 'ether')).buildTransaction(tx_info)
   sos(transfer_tx, key)

print("swear randomly")
for i in range(0, 42*3):
   word = words[random.randrange(0,len(words))]
   id = random.randrange(1, len(users))

   tx_info.update({'nonce': eth.getTransactionCount(users[id])})
   tx_info.update({'from': users[id]})
   swear_tx = jar.functions.swear(word, web3.toWei(1, 'ether')).buildTransaction(tx_info)

   sos(swear_tx, keys[id])

# display map
for id in range(0, len(users)):
   tx_info.update({'nonce': eth.getTransactionCount(users[id])})
   tx_info.update({'from': users[id]})
   data = jar.functions.loosen().call({"from": users[id]})
   print(f"user {users[id]}: {data}")

# withdraw all words
for id in range(0, len(users)):
    for word in words:
        tx_info.update({'nonce': eth.getTransactionCount(users[id])})
        tx_info.update({'from': users[id]})
        redeem_tx = jar.functions.redeem(users[id], word).buildTransaction(tx_info)
        sos(redeem_tx, keys[id])

print(f"Jar reserve: {token.functions.balanceOf(jar_address).call()}")
