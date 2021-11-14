from brownie import FundMe, network, config
from scripts.helpful_scripts import deploy_mocks, get_account, LOCAL_BLOCKCHAIN_ENVIORNMENTS


def  deploy_fund_me():
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
        price_feed_address = config["networks"][network.show_active()]['eth_usd_price_feed']
    else:
        price_feed_address = deploy_mocks()

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config['networks'][network.show_active()].get("verify")
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me;


def main():
    deploy_fund_me()
