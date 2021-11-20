from _pytest.config import exceptions
from brownie import Lottery, accounts, config, network, exceptions
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
import pytest
from scripts.helpful_scripts import fund_with_link, LOCAL_BLOCKCHAIN_ENVIORNMENTS, get_account, get_contract


def test_get_enterance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    # Act
    expected_enterance_fee = Web3.toWei(0.025, 'ether')
    enterance_fee = lottery.getEnteranceFee()
    # Assert
    assert expected_enterance_fee == enterance_fee


def test_cant_enter_unless_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    # Act
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter(
            {
                'from': get_account(),
                'value': lottery.getEnteranceFee()
            }
        )


def test_can_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({'from': account})
    # Act
    lottery.enter({'from': account, 'value': lottery.getEnteranceFee()})
    # Assert
    assert lottery.players(0) == account


def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({'from': account})
    lottery.enter({'from': account, 'value': lottery.getEnteranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({'from': account})
    assert lottery.lottery_state() == 2


def test_can_pick_winner():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({'from': account})
    lottery.enter({'from': account, 'value': lottery.getEnteranceFee()})
    lottery.enter({'from': get_account(index=1),
                  'value': lottery.getEnteranceFee()})
    lottery.enter({'from': get_account(index=2),
                  'value': lottery.getEnteranceFee()})
    lottery.enter({'from': get_account(index=3),
                  'value': lottery.getEnteranceFee()})
    fund_with_link(lottery)
    transaction = lottery.endLottery({'from': account})

    # pretending as a chainlink node to provide random na. equal to static_rng
    request_id = transaction.events['RequestedRandomness']['requestId']
    STATIC_RNG = 18 # 16 % 4 = 0 so 0th account will win the lottery
    winning_account = get_account(index=2)
    starting_balance_of_account = winning_account.balance()
    balance_of_lottery = lottery.balance()
    get_contract('vrf_coordinator').callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address, {'from': account})

    assert lottery.recentWinner() == winning_account
    assert lottery.balance() == 0
    assert winning_account.balance() == starting_balance_of_account + balance_of_lottery
