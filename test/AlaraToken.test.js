const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("AlaraToken", function () {
  let AlaraToken, alaraToken, owner, addr1, addr2;

  beforeEach(async () => {
    [owner, addr1, addr2] = await ethers.getSigners();
    AlaraToken = await ethers.getContractFactory("AlaraToken");
    alaraToken = await AlaraToken.deploy();
    await alaraToken.waitForDeployment();
  });

  it("Should deploy with 8M total supply", async () => {
    const totalSupply = await alaraToken.totalSupply();
    expect(totalSupply).to.equal(ethers.parseEther("8000000"));
  });

  it("Should have correct name and symbol", async () => {
    expect(await alaraToken.name()).to.equal("Alara");
    expect(await alaraToken.symbol()).to.equal("ALA");
  });

  it("Should mint initial supply to owner", async () => {
    const ownerBalance = await alaraToken.balanceOf(owner.address);
    expect(ownerBalance).to.equal(ethers.parseEther("8000000"));
  });

  it("Should deduct 2% fee on transfer from non-owner", async () => {
    // Transfer some tokens to addr1 first
    const transferAmount = ethers.parseEther("1000");
    await alaraToken.transfer(addr1.address, transferAmount);
    
    // Now addr1 transfers to addr2
    const amount = ethers.parseEther("100");
    const initialAddr1Balance = await alaraToken.balanceOf(addr1.address);
    const initialFeeWalletBalance = await alaraToken.balanceOf(owner.address);
    
    await alaraToken.connect(addr1).transfer(addr2.address, amount);
    
    const addr2Balance = await alaraToken.balanceOf(addr2.address);
    const newAddr1Balance = await alaraToken.balanceOf(addr1.address);
    const newFeeWalletBalance = await alaraToken.balanceOf(owner.address);
    
    // addr2 should receive 98 ALA (2% fee)
    expect(addr2Balance).to.equal(ethers.parseEther("98"));
    
    // addr1 should have sent 100 but only 98 went to addr2, 2 went to fee wallet
    expect(newAddr1Balance).to.equal(initialAddr1Balance - amount);
    
    // Fee wallet should have received 2 ALA
    expect(newFeeWalletBalance).to.equal(initialFeeWalletBalance + ethers.parseEther("2"));
  });

  it("Should allow owner to mint new tokens", async () => {
    await alaraToken.mint(addr1.address, ethers.parseEther("1000"));
    const addr1Balance = await alaraToken.balanceOf(addr1.address);
    expect(addr1Balance).to.equal(ethers.parseEther("1000"));
  });

  it("Should not allow non-owner to mint", async () => {
    await expect(
      alaraToken.connect(addr1).mint(addr2.address, ethers.parseEther("100"))
    ).to.be.reverted;
  });

  it("Should allow owner to toggle fee", async () => {
    await alaraToken.toggleFee(false);
    expect(await alaraToken.feeEnabled()).to.equal(false);
    
    await alaraToken.toggleFee(true);
    expect(await alaraToken.feeEnabled()).to.equal(true);
  });

  it("Should allow owner to update fee wallet", async () => {
    await alaraToken.setFeeWallet(addr1.address);
    expect(await alaraToken.feeWallet()).to.equal(addr1.address);
  });

  it("Should not deduct fee for owner transfers", async () => {
    const amount = ethers.parseEther("100");
    const initialOwnerBalance = await alaraToken.balanceOf(owner.address);
    
    await alaraToken.transfer(addr1.address, amount);
    
    const newOwnerBalance = await alaraToken.balanceOf(owner.address);
    const addr1Balance = await alaraToken.balanceOf(addr1.address);
    
    // Owner transfers should NOT have fee
    expect(newOwnerBalance).to.equal(initialOwnerBalance - amount);
    expect(addr1Balance).to.equal(amount);
  });

  it("Should not deduct fee when transferring to owner", async () => {
    // Transfer some tokens to addr1 first
    const transferAmount = ethers.parseEther("1000");
    await alaraToken.transfer(addr1.address, transferAmount);
    
    // addr1 transfers to owner - should NOT have fee
    const amount = ethers.parseEther("100");
    const initialAddr1Balance = await alaraToken.balanceOf(addr1.address);
    const initialOwnerBalance = await alaraToken.balanceOf(owner.address);
    
    await alaraToken.connect(addr1).transfer(owner.address, amount);
    
    const newAddr1Balance = await alaraToken.balanceOf(addr1.address);
    const newOwnerBalance = await alaraToken.balanceOf(owner.address);
    
    // No fee should be deducted
    expect(newAddr1Balance).to.equal(initialAddr1Balance - amount);
    expect(newOwnerBalance).to.equal(initialOwnerBalance + amount);
  });

  it("Should not deduct fee when transferring from fee wallet", async () => {
    // Transfer some tokens to addr1 first
    const transferAmount = ethers.parseEther("1000");
    await alaraToken.transfer(addr1.address, transferAmount);
    
    // Update fee wallet to addr1
    await alaraToken.setFeeWallet(addr1.address);
    
    // addr1 (now fee wallet) transfers to addr2 - should NOT have fee
    const amount = ethers.parseEther("100");
    const initialAddr1Balance = await alaraToken.balanceOf(addr1.address);
    
    await alaraToken.connect(addr1).transfer(addr2.address, amount);
    
    const addr2Balance = await alaraToken.balanceOf(addr2.address);
    const newAddr1Balance = await alaraToken.balanceOf(addr1.address);
    
    // No fee should be deducted
    expect(addr2Balance).to.equal(amount);
    expect(newAddr1Balance).to.equal(initialAddr1Balance - amount);
  });
});
