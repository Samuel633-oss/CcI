"""
Alara Blockchain - Block Implementation
A minimal, Bitcoin-like block structure for the Alara blockchain.
"""

import hashlib
import json
import time
from typing import List, Dict, Any, Optional


class Block:
    """
    Represents a block in the Alara blockchain.
    Each block contains:
    - index: Block height in the chain
    - timestamp: When the block was created
    - transactions: List of transactions in this block
    - previous_hash: Hash of the previous block
    - nonce: Number used for Proof-of-Work
    - hash: This block's hash
    - miner: Address of the miner who mined this block
    - fee_reward: Total fees collected from transactions in this block
    """
    
    def __init__(
        self,
        index: int,
        transactions: List[Dict[str, Any]],
        previous_hash: str,
        miner: str = "0",
        timestamp: Optional[float] = None,
        nonce: int = 0
    ):
        self.index = index
        self.timestamp = timestamp or time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.miner = miner
        self.hash = self.calculate_hash()
        self.fee_reward = self.calculate_fee_reward()
    
    def calculate_hash(self) -> str:
        """
        Calculate the SHA-256 hash of this block.
        This is the core of Proof-of-Work.
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "miner": self.miner
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def calculate_fee_reward(self) -> int:
        """
        Calculate total fees from all transactions in this block.
        Each transaction has a 5% fee that goes to the miner.
        """
        total_fee = 0
        for tx in self.transactions:
            if tx.get("type") == "transaction":
                amount = tx.get("amount", 0)
                fee = int(amount * 0.05)  # 5% fee
                total_fee += fee
        return total_fee
    
    def mine_block(self, difficulty: int) -> None:
        """
        Mine this block by finding a nonce that satisfies the difficulty.
        The hash must start with 'difficulty' number of zeros.
        """
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary for JSON serialization."""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "nonce": self.nonce,
            "miner": self.miner,
            "fee_reward": self.fee_reward
        }
    
    def __repr__(self) -> str:
        return f"Block(index={self.index}, hash={self.hash[:10]}..., miner={self.miner}, fee_reward={self.fee_reward} ALA)"
