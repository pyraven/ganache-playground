// SPDX-License-Identifier: MIT

pragma solidity ^0.8.13;

contract Bank {

    mapping(address => uint) public balances;

    constructor() payable {}

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint _amount) public {
        require(balances[msg.sender] >= _amount);

        (bool sent, ) = msg.sender.call{value: _amount}("");
        require(sent, "Failed to send ether");

        balances[msg.sender] -= _amount;
    }
}