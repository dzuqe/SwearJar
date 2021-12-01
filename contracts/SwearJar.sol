// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract SwearJar {
    struct Swear {
      string word;
      uint256 count;
      uint256 spent;
    }

    mapping(address => Swear []) public swears;
    uint256 private percent = 3;

    uint256 public trashcan;
    address public owner;
    IERC20 SCARG;

    event Swore();
    event Redempt();
    event Trash();
    event Adjust();

    modifier auth() {
      require(msg.sender == owner, "(SwearJar Error): Only the owner access the trash.");
      _;
    }

    constructor(address _owner, address token) {
      owner = _owner;
      SCARG = IERC20(token);
    }

    /**
     * swear - updates an existing word or adds a new one if it doesn't exist
     * @param word
     * @param amount
     */
    function swear(string memory word, uint256 amount) public payable {
      require(bytes(word).length > 0, "(SwearJar Error): You gotta at least swear first, man.");
      require(amount <= SCARG.balanceOf(msg.sender), "You don't have enough $SCARG to swear.");
     
      uint256 index = exists(msg.sender, word);
      if (swears[msg.sender].length != 0 && index < swears[msg.sender].length) {
        swears[msg.sender][index].count += 1;
        swears[msg.sender][index].spent += amount;
        SCARG.transferFrom(msg.sender, address(this), amount);
      } else {
        swears[msg.sender].push(Swear(word, 1, amount));
        SCARG.transferFrom(msg.sender, address(this), amount);
      }
      emit Swore();
    }

    /**
     * exists - checks if the user has already said the word
     * @param sender
     * @param word
     * @returns index
     */
    function exists(address sender, string memory word) private view returns (uint256) {
      uint256 i=0;
      for (i = 0; i < swears[sender].length; i++) {
        if (keccak256(abi.encodePacked(swears[sender][i].word)) == keccak256(abi.encodePacked(word))) {
          return i;
        }
      }
      return i;
    }

    /**
     * loosen - view all your swear words
     * @returns swears
     */
    function loosen() public view returns (Swear [] memory) {
      return swears[msg.sender];
    }

    /**
     * redeem - withdraw amount of SCARG stored in a swear word
     * @param swearer
     * @param word
     */
    function redeem(address payable swearer, string memory word) public payable {
      for (uint256 i = 0; i < swears[swearer].length; i++) {
        if (keccak256(abi.encodePacked(swears[swearer][i].word)) == keccak256(abi.encodePacked(word))) {
          uint256 amount = swears[swearer][i].spent;
          uint256 trash = amount * percent / 100;
          uint256 rcv_amount = amount - trash;

          swears[swearer][i].spent = 0;

          if (SCARG.balanceOf(address(this)) >= rcv_amount) {
            trashcan += trash;
            SCARG.transfer(swearer, rcv_amount);
            break;
          } else
            revert();
        }
      }
      emit Redempt();
    }

    // called when msg.data is not empty
    fallback() external payable {}
    receive() external payable {}

    /**
     * feel - see what's in the trash (only owner)
     */
    function feel() public auth view returns (uint256) {
      return trashcan;
    }

    /**
     * dump - withdraw amount that's in trashcan from contract
     * @param to
     */
    function dump(address payable to) public auth payable {
      require(trashcan >= 0, "(SwearJar Error): No trash to take out.");
      require(address(this).balance >= trashcan, "(SwearJar Error): Not enough balance in the contract.");
      trashcan = 0;
      SCARG.transferFrom(address(this), to, trashcan);
      emit Trash();
    }

    /**
     * adjust - updates the percentage taken from user withdraws
     * @param _percent
     */
    function adjust(uint256 _percent) public auth {
        percent = _percent;
        emit Adjust();
    }

    /**
     * new_auth - sets a new owner of the contract (only owner)
     * @param _owner
     */
    function new_auth(address _owner) public auth {
        owner = _owner;
        emit Adjust();
    }

    /**
     * new_token - updates the connected IERC20 token (only owner)
     * @param token
     */
    function new_token(address token) public auth {
        SCARG = IERC20(token);
    }
}
