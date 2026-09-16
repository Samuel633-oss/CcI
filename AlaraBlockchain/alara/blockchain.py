"""
Alara Blockchain - Core Blockchain Implementation
A decentralized, Proof-of-Work blockchain with fixed 21M ALA supply and 5% transaction fees.
"""

import json
import os
import time
from typing import List, Dict, Any, Optional
from .block import Block


class AlaraBlockchain:
    """
    The main Alara blockchain class.
    Manages the chain of blocks, transactions, and mining.
    
    Features:
    - Fixed 21,000,000 ALA supply (no minting after genesis)
    - 5% transaction fee (burned to reduce supply)
    - Proof-of-Work (SHA-256) consensus
    - Decentralized (P2P networking ready)
    - No admin/owner (fully decentralized)
    """
    
    # Constants
    TOTAL_SUPPLY = 21_000_000  # 21 million ALA, fixed supply
    TRANSACTION_FEE_PERCENT = 5  # 5% fee on every transaction
    MINING_REWARD = 50  # Initial block reward (halves every 210,000 blocks like Bitcoin)
    INITIAL_DIFFICULTY = 4  # Start with 4 leading zeros
    BLOCK_TIME_TARGET = 600  # Target block time in seconds (10 minutes like Bitcoin)
    HALVING_INTERVAL = 210_000  # Blocks between reward halvings
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the Alara blockchain.
        
        Args:
            data_dir: Directory to store blockchain data
        """
        self.data_dir = data_dir
        self.chain: List[Block] = []
        self.pending_transactions: List[Dict[str, Any]] = []
        self.difficulty = self.INITIAL_DIFFICULTY
        self.mining_reward = self.MINING_REWARD
        self.current_block_index = 0
        self.total_supply = 0
        self.miner_balances: Dict[str, int] = {}  # Track miner balances
        self.address_balances: Dict[str, int] = {}  # Track all address balances
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Load existing chain or create genesis block
        if self._chain_file_exists():
            self._load_chain()
        else:
            self._create_genesis_block()
    
    def _chain_file_exists(self) -> bool:
        """Check if blockchain data file exists."""
        return os.path.exists(os.path.join(self.data_dir, "chain.json"))
    
    def _create_genesis_block(self) -> None:
        """
        Create the first block (genesis block) in the chain.
        The genesis block has no previous hash and creates the initial supply.
        """
        # Genesis block transaction: Send initial supply to a burn address
        # (In Bitcoin, Satoshi couldn't spend the genesis block reward)
        genesis_transaction = {
            "type": "genesis",
            "sender": "0",
            "receiver": "0",  # Burn address
            "amount": 0,
            "message": "Alara: A Decentralized Blockchain - Genesis Block",
            "timestamp": time.time()
        }
        
        genesis_block = Block(
            index=0,
            transactions=[genesis_transaction],
            previous_hash="0",
            miner="0",
            timestamp=time.time()
        )
        
        # Genesis block doesn't need mining
        genesis_block.hash = genesis_block.calculate_hash()
        
        self.chain.append(genesis_block)
        self.current_block_index = 1
        self.total_supply = 0  # Supply starts at 0, will be created via mining rewards
        
        # Save the chain
        self._save_chain()
        print(f"✅ Created genesis block: {genesis_block.hash}")
    
    def _load_chain(self) -> None:
        """Load blockchain from disk."""
        with open(os.path.join(self.data_dir, "chain.json"), "r") as f:
            chain_data = json.load(f)
        
        self.chain = [
            Block(
                index=block_data["index"],
                transactions=block_data["transactions"],
                previous_hash=block_data["previous_hash"],
                miner=block_data.get("miner", "0"),
                timestamp=block_data["timestamp"],
                nonce=block_data["nonce"]
            )
            for block_data in chain_data["chain"]
        ]
        
        self.current_block_index = len(self.chain)
        self.difficulty = chain_data.get("difficulty", self.INITIAL_DIFFICULTY)
        self.mining_reward = chain_data.get("mining_reward", self.MINING_REWARD)
        self.total_supply = chain_data.get("total_supply", 0)
        self.miner_balances = chain_data.get("miner_balances", {})
        self.address_balances = chain_data.get("address_balances", {})
        
        print(f"✅ Loaded blockchain with {len(self.chain)} blocks")
    
    def _save_chain(self) -> None:
        """Save blockchain to disk."""
        chain_data = {
            "chain": [block.to_dict() for block in self.chain],
            "difficulty": self.difficulty,
            "mining_reward": self.mining_reward,
            "total_supply": self.total_supply,
            "miner_balances": self.miner_balances,
            "address_balances": self.address_balances
        }
        
        with open(os.path.join(self.data_dir, "chain.json"), "w") as f:
            json.dump(chain_data, f, indent=2)
    
    def get_latest_block(self) -> Block:
        """Get the most recent block in the chain."""
        return self.chain[-1]
    
    def add_transaction(self, sender: str, receiver: str, amount: int) -> Optional[str]:
        """
        Add a new transaction to the pending pool.
        
        Args:
            sender: Sender's address
            receiver: Receiver's address
            amount: Amount of ALA to send
            
        Returns:
            Transaction ID if successful, None if failed
        """
        # Calculate 5% fee
        fee = int(amount * (self.TRANSACTION_FEE_PERCENT / 100))
        total_cost = amount + fee
        
        # Check if sender has enough balance
        sender_balance = self.address_balances.get(sender, 0)
        if sender_balance < total_cost:
            print(f"❌ Insufficient balance. {sender} has {sender_balance} ALA, needs {total_cost}")
            return None
        
        # Create transaction
        transaction = {
            "type": "transaction",
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "fee": fee,
            "total": total_cost,
            "timestamp": time.time(),
            "tx_id": self._generate_tx_id(sender, receiver, amount, time.time())
        }
        
        self.pending_transactions.append(transaction)
        print(f"✅ Transaction added to pool: {transaction['tx_id']}")
        return transaction['tx_id']
    
    def _generate_tx_id(self, sender: str, receiver: str, amount: int, timestamp: float) -> str:
        """Generate a unique transaction ID."""
        tx_string = f"{sender}{receiver}{amount}{timestamp}"
        return hashlib.sha256(tx_string.encode()).hexdigest()[:16]
    
    def mine_pending_transactions(self, miner_address: str) -> Optional[Block]:
        """
        Mine a new block with pending transactions.
        
        Args:
            miner_address: Address of the miner who will receive the reward
            
        Returns:
            The newly mined block, or None if no transactions
        """
        if not self.pending_transactions:
            print("❌ No pending transactions to mine")
            return None
        
        # Create the new block
        new_block = Block(
            index=self.current_block_index,
            transactions=self.pending_transactions,
            previous_hash=self.get_latest_block().hash,
            miner=miner_address
        )
        
        # Mine the block (Proof-of-Work)
        print(f"🔨 Mining block {self.current_block_index}...")
        new_block.mine_block(self.difficulty)
        
        # Add mining reward transaction
        reward_tx = {
            "type": "reward",
            "sender": "0",  # Network reward
            "receiver": miner_address,
            "amount": self.mining_reward + new_block.fee_reward,
            "fee": 0,
            "timestamp": time.time(),
            "tx_id": self._generate_tx_id("0", miner_address, self.mining_reward + new_block.fee_reward, time.time())
        }
        new_block.transactions.append(reward_tx)
        
        # Update balances
        # Process all transactions in the block
        for tx in new_block.transactions:
            if tx["type"] == "transaction":
                sender = tx["sender"]
                receiver = tx["receiver"]
                amount = tx["amount"]
                fee = tx["fee"]
                
                # Deduct from sender
                self.address_balances[sender] = self.address_balances.get(sender, 0) - (amount + fee)
                
                # Add to receiver
                self.address_balances[receiver] = self.address_balances.get(receiver, 0) + amount
                
                # Fee is already included in the miner's reward
            elif tx["type"] == "reward":
                receiver = tx["receiver"]
                amount = tx["amount"]
                self.address_balances[receiver] = self.address_balances.get(receiver, 0) + amount
                self.miner_balances[receiver] = self.miner_balances.get(receiver, 0) + amount
        
        # Update total supply (only from mining rewards, not fees)
        self.total_supply += self.mining_reward
        
        # Check if we need to halve the reward
        if self.current_block_index % self.HALVING_INTERVAL == 0:
            self.mining_reward = max(1, self.mining_reward // 2)  # Halve the reward
            print(f"🎉 Block reward halved to {self.mining_reward} ALA")
        
        # Adjust difficulty based on block time
        if self.current_block_index % 10 == 0:  # Adjust every 10 blocks
            self._adjust_difficulty()
        
        # Add block to chain
        self.chain.append(new_block)
        self.pending_transactions = []
        self.current_block_index += 1
        
        # Save the chain
        self._save_chain()
        
        print(f"✅ Block mined: {new_block.hash}")
        print(f"   Miner: {miner_address}")
        print(f"   Reward: {self.mining_reward} ALA + {new_block.fee_reward} ALA fees")
        print(f"   Total Supply: {self.total_supply} ALA")
        print(f"   Difficulty: {self.difficulty}")
        
        return new_block
    
    def _adjust_difficulty(self) -> None:
        """
        Adjust mining difficulty based on recent block times.
        If blocks are being mined too fast, increase difficulty.
        If too slow, decrease difficulty.
        """
        if len(self.chain) < 2:
            return
        
        # Get last 10 blocks
        recent_blocks = self.chain[-10:]
        
        # Calculate average block time
        total_time = 0
        for i in range(1, len(recent_blocks)):
            total_time += recent_blocks[i].timestamp - recent_blocks[i-1].timestamp
        
        avg_block_time = total_time / (len(recent_blocks) - 1) if len(recent_blocks) > 1 else self.BLOCK_TIME_TARGET
        
        # Adjust difficulty
        if avg_block_time < self.BLOCK_TIME_TARGET * 0.9:  # Blocks too fast
            self.difficulty += 1
        elif avg_block_time > self.BLOCK_TIME_TARGET * 1.1:  # Blocks too slow
            self.difficulty = max(1, self.difficulty - 1)
    
    def get_balance(self, address: str) -> int:
        """Get the balance of an address."""
        return self.address_balances.get(address, 0)
    
    def get_miner_balance(self, address: str) -> int:
        """Get the mining rewards balance of an address."""
        return self.miner_balances.get(address, 0)
    
    def is_chain_valid(self) -> bool:
        """
        Validate the entire blockchain.
        Returns True if valid, False otherwise.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check hash
            if current_block.hash != current_block.calculate_hash():
                print(f"❌ Block {i} hash is invalid")
                return False
            
            # Check previous hash
            if current_block.previous_hash != previous_block.hash:
                print(f"❌ Block {i} previous hash is invalid")
                return False
            
            # Check difficulty
            if current_block.hash[:self.INITIAL_DIFFICULTY] != "0" * self.INITIAL_DIFFICULTY:
                print(f"❌ Block {i} does not meet difficulty requirement")
                return False
        
        return True
    
    def __repr__(self) -> str:
        return f"AlaraBlockchain(blocks={len(self.chain)}, supply={self.total_supply} ALA, difficulty={self.difficulty})"
