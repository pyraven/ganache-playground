import argparse, json
from web3 import Web3

player_one = "0xA17D046D6309F6Ca5b31C2412E376b3CE1F91C78"
player_one_key = "0xdc3439dac3d58a1a569b85e8fe9e33572f6c848b09046a85573cfeafd44ef059"

player_two = "0x817B728218E52eeCE1f0d005DB9a1c40B410F4a9"
player_two_key = "0x07025a567d3f66e0669cf79a5af20b9bb717e4754395a857c1c18502fd54969d"

def get_balance(client, address):
    return client.eth.getBalance(address)

def main():
    
    vuln = json.load(open('Game.json'))

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=True)
    args = parser.parse_args()

    ganache_client = Web3(Web3.HTTPProvider(f"http://{args.host}"))

    vuln_current_balance =  int(Web3.fromWei(get_balance(ganache_client, vuln['Contract Address']), 'ether'))
    player_one_balance =  int(Web3.fromWei(get_balance(ganache_client, player_one), 'ether'))
    player_two_balance =  int(Web3.fromWei(get_balance(ganache_client, player_one), 'ether'))
    print( "*" * 10, "Current Balance", "*" * 10)
    print(
        {
        "Contract Balance": vuln_current_balance, 
        "Player One Balance": player_one_balance, 
        "Player Two Balance" : player_two_balance
        }
    )
    print( "*" * 10, "Current Balance", "*" * 10)

    # player one deposit
    contract_instance = ganache_client.eth.contract(address=vuln['Contract Address'], abi=vuln['Contract ABI'])
    transaction = contract_instance.functions.deposit().buildTransaction(
        {
            "gasPrice": ganache_client.eth.gas_price,
            "chainId": 1337,
            "value": Web3.toWei(1, "ether"),
            "from": player_one,
            "nonce": ganache_client.eth.getTransactionCount(player_one)
        }
    )
    signed_transaction = ganache_client.eth.account.sign_transaction(transaction, private_key = player_one_key)
    transaction_hash = ganache_client.eth.send_raw_transaction(signed_transaction.rawTransaction)
    transaction_receipt = ganache_client.eth.wait_for_transaction_receipt(transaction_hash)
    
    # player two deposit
    contract_instance = ganache_client.eth.contract(address=vuln['Contract Address'], abi=vuln['Contract ABI'])
    transaction = contract_instance.functions.deposit().buildTransaction(
        {
            "gasPrice": ganache_client.eth.gas_price,
            "chainId": 1337,
            "value": Web3.toWei(1, "ether"),
            "from": player_two,
            "nonce": ganache_client.eth.getTransactionCount(player_two)
        }
    )
    signed_transaction = ganache_client.eth.account.sign_transaction(transaction, private_key = player_two_key)
    transaction_hash = ganache_client.eth.send_raw_transaction(signed_transaction.rawTransaction)
    transaction_receipt = ganache_client.eth.wait_for_transaction_receipt(transaction_hash)

    vuln_now_balance =  int(Web3.fromWei(get_balance(ganache_client, vuln['Contract Address']), 'ether'))
    player_one_now_balance =  int(Web3.fromWei(get_balance(ganache_client, player_one), 'ether'))
    player_one_now_balance =  int(Web3.fromWei(get_balance(ganache_client, player_one), 'ether'))
    print( "*" * 10, "Current Balance", "*" * 10)
    print(
        {
        "Contract Balance": vuln_now_balance, 
        "Player One Balance": player_one_now_balance, 
        "Player Two Balance" : player_one_now_balance
        }
    )
    print( "*" * 10, "Current Balance", "*" * 10)

if __name__ == "__main__":

    main()

