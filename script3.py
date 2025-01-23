# wallet balance check

import sys
from web3 import Web3

def check_balance(infura_project_id, wallet_address):
    try:
        web3 = Web3(Web3.HTTPProvider(f"https://sepolia.infura.io/v3/{infura_project_id}"))
        if not web3.is_connected():
            print("Error: Unable to connect to the Ethereum network.")
            return

        balance = web3.eth.get_balance(wallet_address)
        eth_balance = web3.from_wei(balance, 'ether')
        print(f"Balance of the wallet is : {eth_balance} ETH")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script3.py <infura_project_id> <wallet_address>")
    else:
        infura_project_id = sys.argv[1]
        wallet_address = sys.argv[2]
        check_balance(infura_project_id, wallet_address)
