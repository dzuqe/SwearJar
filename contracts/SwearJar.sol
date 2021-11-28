// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract SwearJar {
    struct Swear {
      string word;
      uint256 count;
      uint256 spent;
    }

    uint256 public trashcan;
    mapping(address => Swear []) public swears;
    address public owner;

    constructor(address _owner) {
      owner = _owner;
    }

    modifier onlyOwner() {
      require(msg.sender == owner, "(SwearJar Error): Only the owner access the trash.");
      _;
    }

    function swear(string memory word) public payable {
      require(bytes(word).length > 0, "(SwearJar Error): You gotta at least swear first, man.");
      require(msg.value <= msg.sender.balance, "You don't have enough balance.");

      if (swears[msg.sender].length == 0) {
        swears[msg.sender].push(Swear(word, 1, msg.value));
        return;
      }
     
      uint256 index = wordExists(msg.sender, word);
      if (index < swears[msg.sender].length) {
        swears[msg.sender][index].count += 1;
        swears[msg.sender][index].spent += msg.value;
      } else {
        swears[msg.sender].push(Swear(word, 1, msg.value));
      }
    }

    function wordExists(address sender, string memory word) private view returns (uint256) {
      uint256 i=0;
      for (i = 0; i < swears[sender].length; i++) {
        if (keccak256(abi.encodePacked(swears[sender][i].word)) == keccak256(abi.encodePacked(word))) {
          return i;
        }
      }
      return i;
    }

    function get() public view returns (Swear [] memory) {
      return swears[msg.sender];
    }

    function withdraw(address payable swearer, string memory word) public payable returns (bool) {
      for (uint256 i = 0; i < swears[swearer].length; i++) {
        if (keccak256(abi.encodePacked(swears[swearer][i].word)) == keccak256(abi.encodePacked(word))) {
          uint256 amount = swears[swearer][i].spent;
          uint256 trash = amount * 3 / 100; 
          uint256 rcv_amount = amount - trash;

          swears[swearer][i].spent = 0;

          if (address(this).balance >= rcv_amount) {
            trashcan += trash;
            swearer.transfer(rcv_amount);
            return true;
          } else {
            swears[swearer][i].spent = amount;
            return false;
          }
        }
      }
      return false;
    }

    // called when msg.data is not empty
    fallback() external payable {}
    receive() external payable {}

    function getBalance() public onlyOwner view returns (uint256) {
      return trashcan;
    }

    function trashDay(address payable to) public onlyOwner payable {
      require(trashcan >= 0, "(SwearJar Error): No trash to take out.");
      require(address(this).balance >= trashcan, "(SwearJar Error): Not enough balance in the contract.");
      trashcan = 0;
      to.transfer(trashcan);
    } 
}
