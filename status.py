import argparse
from web3 import Web3

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=True)
    args = parser.parse_args()
    ganache_client = Web3(Web3.HTTPProvider(f"http://{args.host}"))
    if ganache_client.isConnected() == True:
        print("=" * 40)
        print("Ganache Connected")
        print(f"Ganache Block Number: {ganache_client.eth.blockNumber}")
        print(f"Ganache Gas Price: {ganache_client.eth.gasPrice}")
        print(f"# of Ganache Accounts: {len(ganache_client.eth.accounts)}")
        print("=" * 40)

if __name__ == "__main__":

    main()