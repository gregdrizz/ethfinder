import config
from web3 import Web3

w3 = Web3(Web3.HTTPProvider(config.INFURA_URL))

print(w3.eth.block_number)

balance = w3.eth.get_balance("0x334b76f346DdA39af192A6374AD26A5F47b7f160")

transaction = w3.eth.get_transaction("0xd813db7d877f601d121fe848fa405de34cad031a9dd0b164c4c9adadcc624433")

ether_balance = w3.fromWei(balance, 'ether')
print(transaction)