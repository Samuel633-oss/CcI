// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract AlaraToken is ERC20, Ownable {
    uint256 public constant TRANSFER_FEE_PERCENT = 2; // 2% fee
    address public feeWallet;
    bool public feeEnabled = true;

    event FeeWalletUpdated(address newWallet);
    event FeeToggled(bool enabled);

    constructor() ERC20("Alara", "ALA") {
        feeWallet = owner();
        _mint(owner(), 8000000 * 10 ** decimals()); // 8 million ALA
    }

    modifier checkFeeEnabled() {
        require(feeEnabled, "Transfer fees are currently disabled");
        _;
    }

    function setFeeWallet(address _newWallet) external onlyOwner {
        feeWallet = _newWallet;
        emit FeeWalletUpdated(_newWallet);
    }

    function toggleFee(bool _enabled) external onlyOwner {
        feeEnabled = _enabled;
        emit FeeToggled(_enabled);
    }

    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }

    function _transfer(
        address sender,
        address recipient,
        uint256 amount
    ) internal virtual override checkFeeEnabled {
        if (sender != owner() && recipient != owner() && sender != feeWallet) {
            uint256 feeAmount = (amount * TRANSFER_FEE_PERCENT) / 100;
            uint256 amountAfterFee = amount - feeAmount;
            
            require(amountAfterFee > 0, "Transfer amount too small after fee");
            
            super._transfer(sender, feeWallet, feeAmount);
            super._transfer(sender, recipient, amountAfterFee);
        } else {
            super._transfer(sender, recipient, amount);
        }
    }
}
