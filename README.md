# Alara Token (ALA) - ERC-20 with 2% Transfer Fee

**Alara (ALA)** is an ERC-20 token built on Ethereum with a **2% transfer fee**, **mintable** functionality, and **no burn** capability. The total supply is **4.1 million ALA** with **18 decimals**.

## ✅ Features
- **Name:** Alara
- **Symbol:** ALA
- **Total Supply:** 4,100,000 ALA
- **Decimals:** 18
- **Transfer Fee:** 2% (deducted from every transfer)
- **Mintable:** Owner can mint new tokens
- **No Burn:** Users cannot burn tokens
- **Ownable:** Admin control for fee wallet and minting

## 📁 Project Structure
```
.
├── contracts/
│   └── AlaraToken.sol       # ERC-20 Token Contract
├── scripts/
│   └── deploy.js             # Deployment Script
├── hardhat.config.js         # Hardhat Configuration
├── package.json              # Node.js Dependencies
└── README.md
```

## 🚀 Setup & Deployment

### 1. Prerequisites
- [Node.js (v18+)](https://nodejs.org/)
- [Git](https://git-scm.com/)
- [MetaMask](https://metamask.io/) (for real deployments)

### 2. Install Dependencies
```bash
npm install
```

### 3. Local Deployment (Hardhat Network)
```bash
# Compile contracts
npx hardhat compile

# Deploy to local Hardhat network
npx hardhat run scripts/deploy.js
```
- This will deploy to a **local blockchain** (no real gas fees).
- Contract address and details will be saved in `deployment.json`.

### 4. Deploy to a Real Network (Ethereum, Sepolia, etc.)
1. **Get API Keys:**
   - [Infura](https://infura.io/) (for RPC URL)
   - [Etherscan](https://etherscan.io/) (for contract verification)

2. **Update `hardhat.config.js`:**
   ```javascript
   networks: {
     sepolia: {
       url: "https://sepolia.infura.io/v3/YOUR_INFURA_KEY",
       accounts: ["YOUR_PRIVATE_KEY"],
     },
   },
   etherscan: {
     apiKey: "YOUR_ETHERSCAN_API_KEY",
   },
   ```

3. **Deploy to Sepolia (Testnet):**
   ```bash
   npx hardhat run scripts/deploy.js --network sepolia
   ```

4. **Deploy to Ethereum Mainnet:**
   ```bash
   npx hardhat run scripts/deploy.js --network mainnet
   ```
   ⚠️ **Warning:** Mainnet deployment requires **real ETH for gas fees** (~$50–$100).

### 5. Verify Contract on Etherscan
```bash
npx hardhat verify --network sepolia DEPLOYED_CONTRACT_ADDRESS
```

## 📜 Contract Details

### **AlaraToken.sol**
- **Inherits:** ERC-20, Ownable
- **Transfer Fee:** 2% of every transfer (sent to `feeWallet`)
- **Fee Wallet:** Defaults to contract owner (can be updated)
- **Mintable:** Only owner can mint new tokens

### **Key Functions**
| Function | Description |
|----------|-------------|
| `mint(address to, uint256 amount)` | Mint new tokens (owner only) |
| `setFeeWallet(address _newWallet)` | Update fee wallet address (owner only) |
| `toggleFee(bool _enabled)` | Enable/disable transfer fees (owner only) |

### **Fee Logic**
- **2% fee** is deducted from every transfer **except**:
  - Transfers **from/to the owner**
  - Transfers **from/to the fee wallet**
- Example: If you transfer **100 ALA**, the recipient gets **98 ALA**, and **2 ALA** goes to the fee wallet.

## 🔐 Security Notes
- **Audit Recommended:** This contract has not been professionally audited. Use at your own risk.
- **Fee Wallet:** By default, the fee wallet is the contract owner. Update it with `setFeeWallet` if needed.
- **Gas Costs:** Deploying to mainnet requires ETH for gas fees.

## 📊 Example Workflow

### 1. Deploy to Sepolia Testnet
```bash
npx hardhat run scripts/deploy.js --network sepolia
```
Output:
```
AlaraToken deployed to: 0x123...abc
Owner address: 0x456...def
Total supply: 4100000000000000000000000
Fee wallet: 0x456...def
```

### 2. Add Token to MetaMask
1. Open MetaMask
2. Click **Import Token**
3. Paste the deployed contract address (`0x123...abc`)
4. Token symbol (`ALA`) and decimals (`18`) will auto-fill

### 3. Test Transfers
- Send **100 ALA** to a friend.
- They receive **98 ALA** (2% fee deducted).
- Check the fee wallet balance to confirm the **2 ALA** fee.

## 🤝 Contributing
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a Pull Request

## 📄 License
This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
