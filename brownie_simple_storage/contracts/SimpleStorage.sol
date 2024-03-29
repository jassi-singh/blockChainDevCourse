// SPDX-License-Identifier: MIT

pragma solidity >0.6.0 <0.9.0 ;

contract SimpleStorage {
    
    struct People {
        uint256 number;
        string name;
    }
    
    People[] public people;
    uint256 favNum = 0;
    mapping(string=>uint256) public nameToNuber;
    
    function addPeople(uint256 _num,string memory _name) public
    {
        people.push(People({number:_num,name:_name}));
        nameToNuber[_name] = _num;
    }
    
    function getPeople(uint256 index) public view returns(string memory)
    {
        return people[index].name;
    }

    function getFavNum() public view returns(uint256) {
        return favNum;
    }

    function setFavNum(uint256 _num) public {
        favNum = _num;
    }
    
    
}