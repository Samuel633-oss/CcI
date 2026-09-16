// We require the Hardhat Runtime Environment explicitly here. This is optional
// but useful for running the script in a standalone fashion through `node <script>`.
//
// You can also run a script with `npx hardhat run <script>`. If you do that, Hardhat
// will compile your contracts, add the Hardhat Runtime Environment's members to the
// global scope, and execute the script.
const hre = require("hardhat");

async function main() {
  console.log("Deploying AlaraToken contract...");
  
  const AlaraToken = await hre.ethers.getContractFactory("AlaraToken");
  const alaraToken = await AlaraToken.deploy();
  
  await alaraToken.waitForDeployment();
  
  console.log("AlaraToken deployed to:", await alaraToken.getAddress());
  console.log("Owner address:", await alaraToken.owner());
  console.log("Total supply:", (await alaraToken.totalSupply()).toString());
  console.log("Fee wallet:", await alaraToken.feeWallet());
  
  // Save deployment info to a file
  const fs = require('fs');
  const deploymentInfo = {
    contractAddress: await alaraToken.getAddress(),
    owner: await alaraToken.owner(),
    network: hre.network.name,
    totalSupply: (await alaraToken.totalSupply()).toString(),
    feeWallet: await alaraToken.feeWallet(),
    timestamp: new Date().toISOString()
  };
  
  fs.writeFileSync('deployment.json', JSON.stringify(deploymentInfo, null, 2));
  console.log("Deployment info saved to deployment.json");
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
