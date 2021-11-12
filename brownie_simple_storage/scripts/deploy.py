from brownie import accounts, config, SimpleStorage
import os


def deploy_simple_storage():
    account = accounts[0]
    # account = accounts.load("jassi-test")
    # account = accounts.add(config['wallets']['from_key'])

    simple_storage=SimpleStorage.deploy({"from":account})
    favNum = simple_storage.getFavNum()
    print(favNum)

    transaction = simple_storage.setFavNum(13,{"from":account})
    transaction.wait(1)

    favNum = simple_storage.getFavNum()
    print(favNum)


def main():
    deploy_simple_storage()
