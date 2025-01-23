import sys
from web3 import Web3

def check_infura_connection(infura_project_id):
    try:
        # Connect to the Ethereum node via Infura
        web3 = Web3(Web3.HTTPProvider(f"https://sepolia.infura.io/v3/{infura_project_id}"))
        
        # Check if the connection to the node was successful
        if web3.is_connected():
            print("Successfully connected to Infura.")
        else:
            print("Failed to connect to Infura.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script1.py <infura_project_id>")
    else:
        infura_project_id = sys.argv[1]
        check_infura_connection(infura_project_id)
