from brownie.network import account
from scripts.helpful_scripts import get_account
from brownie import FundMe


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fee = fund_me.getEnteranceFee()
    print(f'The current entery fee is {entrance_fee}')
    print("Funding ...")
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
