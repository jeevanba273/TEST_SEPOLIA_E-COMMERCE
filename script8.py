# verify the signature of the transaction

import sys
from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct

# Get Infura Project ID, sender private key, and receiver address from command-line arguments
if len(sys.argv) != 4:
    print("Error: Please provide Infura Project ID, sender private key, and receiver address as arguments.")
    sys.exit(1)

infura_project_id = sys.argv[1]
sender_private_key = sys.argv[2]
receiver_address = sys.argv[3]

def is_valid_address(address):
    return Web3.is_address(address)

def is_valid_private_key(private_key):
    try:
        Account.from_key(private_key)
        return True
    except ValueError:
        return False

# Connect to Sepolia testnet
web3 = Web3(Web3.HTTPProvider(f'https://sepolia.infura.io/v3/{infura_project_id}'))

if not web3.is_connected():
    print("\nFailed to connect to Ethereum node. Please check your connection and try again.")
    sys.exit(1)

print("Successfully connected to Sepolia testnet")

if not is_valid_private_key(sender_private_key):
    print("\nInvalid sender private key. Please check and try again.\n")
    sys.exit(1)

sender_account = Account.from_key(sender_private_key)

if not is_valid_address(receiver_address):
    print("Invalid receiver address. Please check and try again.")
    sys.exit(1)

try:
    # Transaction details
    transaction = {
        'to': receiver_address,
        'value': web3.to_wei(0.01, 'ether'),  # Sending 0.01 ETH
        'gas': 21000,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(sender_account.address),
        'chainId': web3.eth.chain_id
    }

    print("\n--- Sender's End ---\n")

    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(transaction, sender_private_key)

    # Extract v, r, s components of the signature
    v, r, s = signed_txn.v, signed_txn.r, signed_txn.s

    print(f"Transaction Hash: {web3.to_hex(signed_txn.hash)}")
    print(f"v: {v}")
    print(f"r: {web3.to_hex(r)}")
    print(f"s: {web3.to_hex(s)}")

    print("\n\n--- Receiver's End ---\n")

    # Recover the sender's address from the signature components
    recovered_address = web3.eth.account.recover_transaction(signed_txn.rawTransaction)

    print(f"Recovered sender's address: {recovered_address}")
    print(f"Actual sender's address: {sender_account.address}")

    if recovered_address.lower() == sender_account.address.lower():
        print("\nThe signature is valid. The transaction was indeed signed by the sender.")
    else:
        print("\nThe signature is invalid or does not match the sender's address.")

    # Check if the recovered address has sufficient balance
    sender_balance = web3.eth.get_balance(recovered_address)
    if sender_balance >= transaction['value'] + (transaction['gas'] * transaction['gasPrice']):
        print("\nThe sender has sufficient balance for this transaction.\n")
    else:
        print("\nThe sender does not have sufficient balance for this transaction.\n")

except ValueError as e:
    print(f"An error occurred while processing the transaction: {str(e)}\n")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}\n")