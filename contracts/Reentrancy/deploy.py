import argparse, json
from web3 import Web3
from solcx import compile_standard, install_solc

address_one = "0x7a52E1A7e0ca1C863FC9C476Ff6F27545E619C2e"
address_one_key = "0x3e5146d9872998bb404ad910ac9bd7e7dec397be57580f2d0284e8c92e69e71b"

_solc_version = "0.8.13"
install_solc(_solc_version)

def get_balance(client, address):
    return client.eth.getBalance(address)

def open_contract(filepath):
    with open(filepath, 'r') as file:
        contract_file = file.read()
        return contract_file
    
def compile_contract(contract_name, contract):
    compiled = compile_standard({
        "language": "Solidity",
        "sources": { contract_name: {
            "content": contract
        }},
        "settings": {
            "outputSelection": {
                "*": {"*":
                      ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        }
    }, solc_version = "0.8.13")
    return compiled

def deploy_vuln_contract(client, contract_name, wallet_address, wallet_key, abi, bytecode):
    contract = client.eth.contract(abi=abi, bytecode=bytecode)
    nonce = client.eth.getTransactionCount(wallet_address)
    transaction = contract.constructor().buildTransaction(
        {
            "gasPrice": client.eth.gas_price,
            "chainId": 1337,
            "value": Web3.toWei(10, "ether"),
            "from": wallet_address,
            "nonce": nonce
        }
    )
    signed_transaction = client.eth.account.sign_transaction(transaction, private_key = wallet_key)
    transaction_hash = client.eth.send_raw_transaction(signed_transaction.rawTransaction)
    transaction_receipt = client.eth.wait_for_transaction_receipt(transaction_hash)
    balance = get_balance(client, transaction_receipt['contractAddress'])
    deployed = {
        "Contract Name": contract_name, 
        "Contract Address" : transaction_receipt['contractAddress'],
        "Contract Balance": int(Web3.fromWei(balance, 'ether')),
        "Contract ABI": abi
    }
    print(deployed)
    with open(f"{contract_name}.json", "w") as json_file:
        json.dump(deployed, json_file)
    return transaction_receipt['contractAddress']

def deploy_attack_contract(client, contract_name, wallet_address, wallet_key, abi, bytecode, contract_address):
    contract = client.eth.contract(abi=abi, bytecode=bytecode)
    nonce = client.eth.getTransactionCount(wallet_address)
    transaction = contract.constructor(contract_address).buildTransaction(
        {
            "gasPrice": client.eth.gas_price,
            "chainId": 1337,
            "from": wallet_address,
            "nonce": nonce
        }
    )
    signed_transaction = client.eth.account.sign_transaction(transaction, private_key = wallet_key)
    transaction_hash = client.eth.send_raw_transaction(signed_transaction.rawTransaction)
    transaction_receipt = client.eth.wait_for_transaction_receipt(transaction_hash)
    balance = get_balance(client, transaction_receipt['contractAddress'])
    deployed = {
        "Contract Name": contract_name, 
        "Contract Address" : transaction_receipt['contractAddress'],
        "Contract Balance": int(Web3.fromWei(balance, 'ether')),
        "Contract ABI": abi
    }
    print(deployed)
    with open(f"{contract_name}.json", "w") as json_file:
        json.dump(deployed, json_file)
    return

def main():

    contracts = ["Bank.sol", "AttackBank.sol"]

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=True)
    args = parser.parse_args()

    vuln_contract_address = ""
    for contract in contracts:
        contract_name = contract.split('.')[0]
        contract_string = open_contract(contract)
        compiled_contract = compile_contract(contract_name, contract_string)
        contract_abi = compiled_contract['contracts'][contract_name][contract_name]['abi']
        contract_bytecode = compiled_contract['contracts'][contract_name][contract_name]['evm']['bytecode']['object']
        ganache_client = Web3(Web3.HTTPProvider(f"http://{args.host}"))
        if contract == "Bank.sol":
            vuln_contract_address = deploy_vuln_contract(ganache_client, contract_name, address_one, address_one_key, contract_abi, contract_bytecode)
        else:
            deploy_attack_contract(ganache_client, contract_name, address_one, address_one_key, contract_abi, contract_bytecode, vuln_contract_address)

if __name__ == "__main__":

    main()