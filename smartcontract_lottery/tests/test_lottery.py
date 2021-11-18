from brownie import Lottery, accounts, config, network
from web3 import Web3

def test_get_enterance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config['networks'][network.show_active()]['eth_usd_price_feed'],
        {"from": account},
    )
    assert lottery.getEnteranceFee() > Web3.toWei(0.010,"ether")
    assert lottery.getEnteranceFee() < Web3.toWei(0.012, "ether")
