require("@nomicfoundation/hardhat-toolbox");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.20",
  networks: {
    hardhat: {
      // Local Hardhat network settings
      chainId: 31337,
      accounts: {
        mnemonic: "test test test test test test test test test test test junk",
      },
    },
    sepolia: {
      url: "https://sepolia.infura.io/v3/YOUR_INFURA_KEY",
      accounts: ["YOUR_PRIVATE_KEY"],
    },
    mainnet: {
      url: "https://mainnet.infura.io/v3/YOUR_INFURA_KEY",
      accounts: ["YOUR_PRIVATE_KEY"],
    },
  },
  etherscan: {
    apiKey: "YOUR_ETHERSCAN_API_KEY",
  },
};
