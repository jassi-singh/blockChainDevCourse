from brownie import  SimpleStorage ,accounts


def test_deploy():
    # Arrange
    account = accounts[0]

    # Act
    simple_storage = SimpleStorage.deploy({"from":account})
    intial_value = simple_storage.getFavNum()
    expected = 0

    #Assert
    assert intial_value == expected

def test_updating_stoarge():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})

    # Act
    simple_storage.setFavNum(13,{"from": account}).wait(1)
    expected = 13

    #Assert
    assert simple_storage.getFavNum() == expected
