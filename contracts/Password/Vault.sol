// SPDX-License-Identifier: MIT

pragma solidity ^0.8.13;

contract Vault {

    string private username;
    bytes32 private password;

    constructor(string memory _username, bytes32 _password) {
        username = _username;
        password = _password;
    }
}