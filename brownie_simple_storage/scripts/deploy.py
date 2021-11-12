from brownie import accounts, config, SimpleStorage, network
import os


def deploy_simple_storage():
    account = get_account()

    simple_storage = SimpleStorage.deploy({"from": account})
    favNum = simple_storage.getFavNum()
    print(favNum)

    transaction = simple_storage.setFavNum(13, {"from": account})
    transaction.wait(1)

    favNum = simple_storage.getFavNum()
    print(favNum)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])


def main():
    deploy_simple_storage()
