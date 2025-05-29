// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Bank {
    uint public balance = 0;

    function deposit(uint amount) public payable {
        balance += amount;
    }
/* 
    function withdraw(uint amount) public {
        balance -= amount;
    }
 */
    function getBalance() public view returns (uint) {
        return balance;
    }
}