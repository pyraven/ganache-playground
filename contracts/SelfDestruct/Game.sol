// SPDX-License-Identifier: MIT

pragma solidity ^0.8.13;

contract Game {

    uint public targetBalance = 7 ether;
    address public winner;

    constructor() {}

    function deposit() public payable {
        require(msg.value == 1 ether, "You must only send 1 ether");

        uint balance = address(this).balance;
        require(balance <= targetBalance, "Game is over");

        if (balance == targetBalance) {
            winner = msg.sender;
        }
    }

    function claimReward() public {
        require(msg.sender == winner, "You are not the winner");

        (bool sent, ) = msg.sender.call{value: address(this).balance}("");
        require(sent, "Failed to send Ether");
    }
}