// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Bank {
    uint public balance = 0;
    address private owner;

    constructor() {
        owner = msg.sender;
    }

    function deposit(uint amount) public payable {
        balance += amount;
    }

    function withdraw(uint amount) public {
        balance -= amount;
    }

    function getBalance() public view returns (uint) {
        return balance;
    }

    function getOwner() public view returns (address) {
        require(msg.sender == owner, "Only owner can call this function");
        return owner;
    }
}