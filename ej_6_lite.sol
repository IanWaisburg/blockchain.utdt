// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Loteria {
    uint256 public ticketPrice;
    uint256 public totalTickets;
    uint256 public ticketsSold;
    mapping(address => uint256) public ticketsBought;
    
    function buyTickets(uint256 numberOfTickets) public payable {
        require(numberOfTickets > 0, "Must buy at least one ticket");
        require(ticketsBought[msg.sender] + numberOfTickets <= totalTickets, "Not enough tickets available");
        require(msg.value == ticketPrice * numberOfTickets, "Incorrect amount sent");
        
        ticketsBought[msg.sender] += numberOfTickets;
        ticketsSold += numberOfTickets;
    }
    
    function getMyTickets() public view returns (uint256) {
        return ticketsBought[msg.sender];
    }
    
    function getTotalTicketsSold() public view returns (uint256) {
        return ticketsSold;
    }
    
    function getContractBalance() public view returns (uint256) {
        return address(this).balance;
    }
}