# generate an etherium address and a private key

from web3 import Web3

# Generate a new Ethereum account
account = Web3().eth.account.create()

# Print the new account's address and private key
print(f"Address: {account.address}")
print(f"Private Key: {account._private_key.hex()}")
