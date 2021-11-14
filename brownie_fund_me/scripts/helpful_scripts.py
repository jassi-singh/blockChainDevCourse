from brownie import network, accounts, config, MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_BLOCKCHAIN = ['mainnet-fork']
LOCAL_BLOCKCHAIN_ENVIORNMENTS = ['development', 'ganache-local']

DECIMALS = 8
STARTINGPRICE = 200000000000


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIORNMENTS or network.show_active() in FORKED_LOCAL_BLOCKCHAIN:
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])


def deploy_mocks():
    print(f'The active network is {network.show_active()}')
    print('Deploying Mocks....')
    MockV3Aggregator.deploy(
        DECIMALS, STARTINGPRICE, {"from": get_account()}
    )
    print("Mocks Deployed")
    return MockV3Aggregator[-1].address
