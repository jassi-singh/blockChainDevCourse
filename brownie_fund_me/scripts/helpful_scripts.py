from brownie import network, accounts, config, MockV3Aggregator
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIORNMENTS = ['development','ganache-local']

DECIMALS = 18
STARTINGPRICE = 2000


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])


def deploy_mocks():
    print(f'The active network is {network.show_active()}')
    print('Deploying Mocks....')
    MockV3Aggregator.deploy(
        DECIMALS, Web3.toWei(STARTINGPRICE, 'ether'), {"from": get_account()}
    )
    print("Mocks Deployed")
    return MockV3Aggregator[-1].address
