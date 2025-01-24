from flask import Flask, request, jsonify
from web3 import Web3

app = Flask(__name__)

@app.route('/connect', methods=['POST'])
def connect_to_infura():
    try:
        # Parse the JSON body to get the Infura project ID
        data = request.get_json()
        if not data or 'infura_project_id' not in data:
            return jsonify({"error": "Missing 'infura_project_id' in request body"}), 400

        infura_project_id = data['infura_project_id']

        # Connect to the Ethereum node via Infura
        web3 = Web3(Web3.HTTPProvider(f"https://sepolia.infura.io/v3/{infura_project_id}"))

        # Check if the connection to the node was successful
        if web3.is_connected():
            return jsonify({"message": "Successfully connected to Infura."}), 200
        else:
            return jsonify({"error": "Failed to connect to Infura."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-wallet', methods=['POST'])
def create_and_send_wallet():
    try:
        # Parse the JSON body to get the Infura project ID
        data = request.get_json()
        if not data or 'infura_project_id' not in data:
            return jsonify({"error": "Missing 'infura_project_id' in request body"}), 400

        infura_project_id = data['infura_project_id']

        # Connect to the Ethereum node via Infura
        web3 = Web3(Web3.HTTPProvider(f"https://sepolia.infura.io/v3/{infura_project_id}"))

        # Generate a new Ethereum account
        account = web3.eth.account.create()

        # Check if account is created successfully
        if account and account.address and account._private_key:
            return jsonify({"sender_address": account.address, "sender_private_key": account._private_key.hex()}), 200
        else:
            return jsonify({"error": "Failed to generate wallet credentials"}), 500
            
@app.route('/get-wallet-balance', methods=['POST'])
def get_balance():
    try:
        # Parse the JSON body to get the Infura project ID
        data = request.get_json()
        if not data or 'infura_project_id' not in data:
            return jsonify({"error": "Missing 'infura_project_id' in request body"}), 400
        if not data or 'sender_address' not in data:
            return jsonify({"error": "Missing 'sender_address' in request body"}), 400

        infura_project_id = data['infura_project_id']
        sender_address = data['sender_address']
            
        web3 = Web3(Web3.HTTPProvider(f"https://sepolia.infura.io/v3/{infura_project_id}"))
        
        if not web3.is_connected():
            print("Error: Unable to connect to the Ethereum network.")
            return jsonify({"error": "Cannot connect to Ethereum network"}), 400

        balance = web3.eth.get_balance(sender_address)
        eth_balance = web3.from_wei(balance, 'ether')
        return jsonify({"balance": eth_balance}), 200
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
