// SPDX-License-Identifier: MIT

pragma solidity >=0.6.6 <0.9.0 ;
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    
    mapping(address => uint256) public addressToAmountFunded;
    address public owner;
    address[] funders;
    AggregatorV3Interface public priceFeed;
    constructor (address _priceFeed) {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }
    
    function fund() public payable {
        uint256 minimumUSD = 50 * 10 ** 18;
        require(getConversionRate(msg.value)>=minimumUSD,"You need to spend more ETH!");
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    } 
    
    function getVersion() public view returns (uint256){
        return priceFeed.version();
    }
    
    function getPriceFeed() public view returns(uint256){
        (
            ,int price,,,
        ) = priceFeed.latestRoundData();
        return uint256(price*10000000000);
    }
    
    function getConversionRate (uint256 ethAmount) public view returns(uint256) {
        uint256 ethPrice = getPriceFeed();
        uint256 ethAmountUsd = (ethPrice*ethAmount)/1000000000000000000;
        return ethAmountUsd;
    }
    
    modifier onlyOwner { 
         require(msg.sender == owner);
         _;
    }
    function withdraw() public onlyOwner payable {
        payable (msg.sender).transfer(address(this).balance);
        for(uint256 i=0;i<funders.length ;i++)
        {
            address funder = funders[i];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
    }

    function getEnteranceFee() public view returns (uint256) {
        uint256 minimumUSD = 50 * 10 ** 18;
        uint256 price = getPriceFeed();
        uint256 precison = 1 * 10**18;
        return (minimumUSD * precison)/price;
    }
}