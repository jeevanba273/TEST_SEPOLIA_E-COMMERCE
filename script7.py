# live track a wallet

import sys
from web3 import Web3, HTTPProvider
import time

# Get Infura Project ID and wallet address from command-line arguments
if len(sys.argv) != 3:
    print("Error: Please provide Infura Project ID and wallet address as arguments.")
    sys.exit(1)

infura_project_id = sys.argv[1]
wallet_address = sys.argv[2]

# Infura endpoint for Sepolia
infura_url = f"https://sepolia.infura.io/v3/{infura_project_id}"

# Connect to Infura
web3 = Web3(HTTPProvider(infura_url))

# Check connection
if not web3.is_connected():
    print("Failed to connect to Infura")
    sys.exit(1)

print("Successfully connected to Infura (Sepolia)")

# Convert wallet address to checksum address
wallet_address = web3.to_checksum_address(wallet_address)

def get_transaction_details(tx):
    receipt = web3.eth.get_transaction_receipt(tx["hash"])
    return {
        "blockNumber": tx["blockNumber"],
        "from": tx["from"],
        "to": tx["to"],
        "value": web3.from_wei(tx["value"], "ether"),
        "hash": tx["hash"].hex(),
        "gasUsed": receipt["gasUsed"],
        "status": receipt["status"]
    }

def print_transaction_details(tx):
    print(f"\nNew transaction found:")
    print(f"Block: {tx['blockNumber']}")
    print(f"From: {tx['from']}")
    print(f"To: {tx['to']}")
    print(f"Value: {tx['value']} ETH")
    print(f"Transaction Hash: {tx['hash']}")
    print(f"Gas Used: {tx['gasUsed']}")
    print(f"Status: {'Success' if tx['status'] == 1 else 'Failed'}")
    sys.stdout.flush()  # Ensure the output is sent immediately

def monitor_transactions(address):
    print(f"Starting to monitor transactions for address: {address}")
    sys.stdout.flush()
    last_checked_block = web3.eth.block_number

    while True:
        try:
            latest_block = web3.eth.block_number
            if latest_block > last_checked_block:
                for block_number in range(last_checked_block + 1, latest_block + 1):
                    print(f"Checking block {block_number}")
                    sys.stdout.flush()
                    block = web3.eth.get_block(block_number, full_transactions=True)
                    for tx in block.transactions:
                        if tx["from"].lower() == address.lower() or (tx["to"] and tx["to"].lower() == address.lower()):
                            tx_details = get_transaction_details(tx)
                            print_transaction_details(tx_details)
                
                last_checked_block = latest_block
            
            time.sleep(10)  # Wait for 10 seconds before checking for new blocks
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.stdout.flush()
            time.sleep(10)  # Wait for 10 seconds before retrying

# Start monitoring transactions
monitor_transactions(wallet_address)