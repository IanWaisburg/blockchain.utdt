import sys
import os
from dotenv import load_dotenv
from web3 import Web3
from solcx import compile_source, install_solc
from pathlib import Path
import json

# 1. Load private key and RPC URL from .env
def load_env():
    load_dotenv()  # Loads environment variables from .env file
    private_key = os.getenv("PRIVATE_KEY")
    rpc_url = os.getenv("RPC_URL")
    
    if not private_key or not rpc_url:
        if not private_key:
            print("❌ PRIVATE_KEY not found in .env file.")
        if not rpc_url:
            print("❌ RPC_URL not found in .env file.")
        sys.exit(1)
    return private_key, rpc_url

# 2. Load smart contract from the file path (CLI argument)
def load_contract(file_path: str, solc_version: str = "0.8.20"):
    install_solc(solc_version)

    source = Path(file_path).read_text()
    compiled = compile_source(source, solc_version=solc_version)
    _, interface = compiled.popitem()

    return interface['abi'], interface['bin']

# 3. Compile contract source file to get ABI and bytecode using solcx
def update_contracts_json(contract_name: str, address: str, abi: list):
    """Update contracts.json with new contract information"""
    contracts_file = 'contracts.json'
    
    # Load existing contracts or create new dict
    if os.path.exists(contracts_file):
        with open(contracts_file, 'r') as f:
            contracts = json.load(f)
    else:
        contracts = {}
    
    # Update or add new contract
    contracts[contract_name] = {
        "address": address,
        "abi": abi
    }
    
    # Write back to file
    with open(contracts_file, 'w') as f:
        json.dump(contracts, f, indent=4)
    
    print(f"✅ Updated {contracts_file} with {contract_name} contract information")

# 4. Deploy contract to Sepolia
def deploy_contract(w3, abi, bytecode, private_key, contract_name: str, constructor_args=None):
    account = w3.eth.account.from_key(private_key)
    address = account.address

    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.get_transaction_count(address)

    txn = contract.constructor(*(constructor_args or [])).build_transaction({
        'from': address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': w3.to_wei('15', 'gwei'),
        'chainId': w3.eth.chain_id
    })

    signed = w3.eth.account.sign_transaction(txn, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)

    print("Deploying contract... TX Hash:", tx_hash.hex())
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("✅ Contract deployed at:", receipt.contractAddress)

    # Update contracts.json with the new contract information
    update_contracts_json(contract_name, receipt.contractAddress, abi)

    return receipt.contractAddress

# 5. Main function to execute the deployment    
if __name__ == "__main__":

    # Input your configuration here
    private_key, rpc_url = load_env()

    # 2. Load contract file path from CLI argument
    if len(sys.argv) != 2:
        sys.exit("❌ Please provide the contract file path as a CLI argument.\nExample: python deployer.py Ej3.sol")
    
    sol_file = sys.argv[1]
    # Extract contract name from filename (remove .sol extension)
    contract_name = Path(sol_file).stem
    solc_version = "0.8.20"

    # 3. Load contract ABI and Bytecode
    try:
        abi, bytecode = load_contract(sol_file, solc_version)
    except Exception as e:
        sys.exit(f"❌ Error loading contract: {e}")

    # 4. Connect to Sepolia
    w3 = Web3(Web3.HTTPProvider(rpc_url))

    if not w3.is_connected():
        sys.exit("❌ Failed to connect to network")

    # 5. Deploy the contract
    deploy_contract(w3, abi, bytecode, private_key, contract_name)