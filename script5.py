# find the latest trasaction

import sys
from web3 import Web3, HTTPProvider
from requests.exceptions import RequestException

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

def find_latest_transaction(address, max_blocks=1000):
    print(f"Searching for the latest transaction for address: {address}")
    latest_block = web3.eth.block_number
    print(f"Latest block number: {latest_block}")

    start_block = max(0, latest_block - max_blocks)

    for block_number in range(latest_block, start_block - 1, -1):
        print(f"Checking block {block_number}...")
        try:
            block = web3.eth.get_block(block_number, full_transactions=True)
            
            for tx in block.transactions:
                if tx["from"].lower() == address.lower() or (tx["to"] and tx["to"].lower() == address.lower()):
                    return get_transaction_details(tx)
        
        except RequestException as e:
            print(f"Request error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    return None

# Find the latest transaction for the wallet address
latest_transaction = find_latest_transaction(wallet_address)

if latest_transaction:
    print("\nLatest transaction found:")
    print(f"Block: {latest_transaction['blockNumber']}")
    print(f"From: {latest_transaction['from']}")
    print(f"To: {latest_transaction['to']}")
    print(f"Value: {latest_transaction['value']} ETH")
    print(f"Transaction Hash: {latest_transaction['hash']}")
    print(f"Gas Used: {latest_transaction['gasUsed']}")
    print(f"Status: {'Success' if latest_transaction['status'] == 1 else 'Failed'}\n")
else:
    print("\nNo transactions found in the specified range.")