// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6 ;
import '@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol';
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase, Ownable{

    address payable[] public players;
    address payable public recentWinner;
    uint256 public randomness;
    uint256 public usdEnteryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;
    uint256 public fee;
    bytes32 keyhash;
    event RequestedRandomness(bytes32 requestId);
    constructor(
        address price_feed_address,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinator,_link) {
        usdEnteryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(price_feed_address);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        require(lottery_state == LOTTERY_STATE.OPEN,"LOTTERY IS NOT OPEN");
        require(msg.value >= getEnteranceFee(), "NOT ENOUGH ETH");
        players.push(payable(msg.sender));
    }

    function getEnteranceFee() public view returns(uint256) {
        (,int256 price,,,) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10**10;
        uint256 costToEnter = uint256(usdEnteryFee * 10**18)/ adjustedPrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner{
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "Can't start a new lottery yet !"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner{
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyhash,fee);
        emit RequestedRandomness(requestId);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness) internal override{
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "You are not there yer"
        );
        require(
            _randomness > 0,
            "randomness not found"
        );
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];

        recentWinner.transfer(address(this).balance);

        // RESET
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }
}