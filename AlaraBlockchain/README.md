# Alara Blockchain (ALA)

**A Decentralized Proof-of-Work Blockchain with Fixed 21M Supply and 5% Transaction Fees**

```
    █████╗ ██╗     ██████╗ █████╗ ██╗   ██╗
   ██╔══██╗██║     ██╔══██╗██╔══██╗╚██╗ ██╔╝
   ███████║██║     ██║  ██║███████║ ╚████╔╝
   ██╔══██║██║     ██║  ██║██╔══██║  ╚██╔╝
   ██║  ██║███████╗██████╔╝██║  ██║   ██║
   ╚═╝  ╚═╝╚══════╝╚═════╝╚═╝  ╚═╝   ╚═╝
```

## ✅ Features

- **Decentralized**: No single point of control, fully peer-to-peer
- **Proof-of-Work**: SHA-256 mining (CPU-mineable)
- **Fixed Supply**: **21,000,000 ALA** (no minting, no printing)
- **Transaction Fees**: **5%** fee on every transaction
- **Block Rewards**: Miners earn ALA + transaction fees
- **Halving**: Block rewards halve every 210,000 blocks (like Bitcoin)
- **Adjustable Difficulty**: Automatically adjusts based on network hashrate

## 📁 Project Structure

```
alara/
├── __init__.py          # Package initialization
├── __main__.py          # Allows running with `python -m alara`
├── block.py             # Block implementation
├── blockchain.py        # Core blockchain logic
├── main.py              # CLI entry point
└── network.py           # P2P networking

assets/
└── alara_logo.png       # Alara logo

requirements.txt         # Python dependencies
README.md               # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Clone the repository
git clone https://github.com/Samuel633-oss/CcI.git
cd CcI/AlaraBlockchain

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Blockchain

```bash
# Run the CLI
python -m alara

# Or run main.py directly
python alara/main.py
```

### 3. Basic Commands

| Command | Description |
|---------|-------------|
| `python -m alara` | Show help |
| `python -m alara mine [address]` | Mine a new block |
| `python -m alara send [from] [to] [amount]` | Send ALA to an address |
| `python -m alara balance [address]` | Check address balance |
| `python -m alara status` | Show blockchain status |
| `python -m alara validate` | Validate the entire chain |

### 4. Example Workflow

```bash
# Start by mining the first block (genesis is already created)
python -m alara mine miner1

# Send some ALA from miner1 to user1
python -m alara send miner1 user1 100

# Mine a block to include the transaction
python -m alara mine miner1

# Check balances
python -m alara balance miner1
python -m alara balance user1

# Check blockchain status
python -m alara status
```

## 🔧 Technical Details

### Blockchain Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| **Total Supply** | 21,000,000 ALA | Fixed supply, no minting |
| **Transaction Fee** | 5% | Fee deducted from every transaction |
| **Initial Block Reward** | 50 ALA | Reward for mining a block |
| **Halving Interval** | 210,000 blocks | Reward halves every 210K blocks |
| **Initial Difficulty** | 4 | Number of leading zeros required |
| **Target Block Time** | 600 seconds | ~10 minutes per block |
| **Hash Algorithm** | SHA-256 | Same as Bitcoin |

### Consensus Mechanism

- **Proof-of-Work (PoW)**: Miners compete to find a nonce that produces a hash with the required number of leading zeros.
- **Difficulty Adjustment**: Automatically adjusts every 10 blocks based on average block time.
- **No Pre-Mine**: The genesis block creates no coins. All ALA is earned through mining.

### Transaction Flow

1. User creates a transaction (sender, receiver, amount)
2. 5% fee is calculated and added to the total cost
3. Transaction is added to the pending pool
4. Miner includes pending transactions in a new block
5. Miner solves the PoW puzzle
6. Block is added to the chain
7. Miner receives the block reward + all transaction fees
8. Balances are updated

### Supply Economics

- **Total Supply**: 21,000,000 ALA (fixed, cannot be changed)
- **Supply Source**: Only from mining rewards (50 ALA initially, halves over time)
- **Fee Burning**: Transaction fees are **added to the miner's reward**, not burned
- **No Minting**: There is **no function** to create new ALA out of thin air

## 🌐 P2P Networking

The blockchain includes a **basic P2P networking layer** (`network.py`) that allows:

- Running a node on a specific host/port
- Connecting to other peers
- Broadcasting blocks and transactions
- Synchronizing the blockchain

### Starting a Node

```python
from alara.blockchain import AlaraBlockchain
from alara.network import AlaraNode

# Create blockchain
blockchain = AlaraBlockchain()

# Create and start a node
node = AlaraNode(blockchain, host="0.0.0.0", port=5000)
node.start()

# Keep the node running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    node.stop()
```

### Connecting to Peers

```python
# Add a peer
node.add_peer("peer1.alara.net", 5000)

# Connect to the peer
node.connect_to_peer("peer1.alara.net", 5000)
```

## 📊 Blockchain Data

All blockchain data is stored in the `alara_data/` directory:

- `chain.json`: The complete blockchain with all blocks, transactions, and balances
- The data persists between runs

## 🔐 Security Notes

1. **No Admin Keys**: This blockchain has **no admin functions**. No one can print or mint new ALA.
2. **Fixed Supply**: The 21M ALA supply is **hardcoded** and cannot be changed.
3. **5% Fee**: All transactions have a **mandatory 5% fee** that goes to miners.
4. **Proof-of-Work**: Security comes from the computational work required to mine blocks.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## 📜 License

This project is **open-source** and free to use. See [LICENSE](LICENSE) for details.

## 💬 Community

- **GitHub**: [Samuel633-oss/CcI](https://github.com/Samuel633-oss/CcI)
- **Issues**: Report bugs and request features on GitHub

---

**Alara Blockchain - Decentralized. Fixed. Fair.**
