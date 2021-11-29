from brownie import network, accounts, config

FORKED_LOCAL_BLOCKCHAIN = ['mainnet-fork']
LOCAL_BLOCKCHAIN_ENVIORNMENTS = ['development', 'ganache-local']


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIORNMENTS
        or network.show_active() in FORKED_LOCAL_BLOCKCHAIN
    ):
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])
