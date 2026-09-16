#!/usr/bin/env python3
"""
Alara Blockchain - Main Entry Point
A decentralized Proof-of-Work blockchain with 21M ALA supply and 5% transaction fees.

Usage:
    python main.py mine [miner_address]    # Mine a new block
    python main.py send [sender] [receiver] [amount]  # Send ALA
    python main.py balance [address]        # Check balance
    python main.py status                  # Show blockchain status
    python main.py validate                 # Validate the chain
"""

import sys
import time
from .blockchain import AlaraBlockchain


def print_header():
    """Print Alara Blockchain header."""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║         █████╗ ██╗     ██████╗ █████╗ ██╗   ██╗                 ║
    ║        ██╔══██╗██║     ██╔══██╗██╔══██╗╚██╗ ██╔╝                 ║
    ║        ███████║██║     ██║  ██║███████║ ╚████╔╝                  ║
    ║        ██╔══██║██║     ██║  ██║██╔══██║  ╚██╔╝                   ║
    ║        ██║  ██║███████╗██████╔╝██║  ██║   ██║                    ║
    ║        ╚═╝  ╚═╝╚══════╝╚═════╝╚═╝  ╚═╝   ╚═╝                    ║
    ║                                                               ║
    ║        Decentralized Proof-of-Work Blockchain                ║
    ║        Fixed Supply: 21,000,000 ALA                            ║
    ║        Transaction Fee: 5%                                   ║
    ║        No Minting, No Admin, Fully Decentralized             ║
    ║                                                               ║
    ╚══════════════════════════════════════════════════════════════╝
    """)


def main():
    """Main entry point for the Alara Blockchain CLI."""
    blockchain = AlaraBlockchain(data_dir="alara_data")
    
    # Print header if no arguments
    if len(sys.argv) == 1:
        print_header()
        print("\n📚 Available Commands:")
        print("  mine [address]       - Mine a new block")
        print("  send <from> <to> <amount> - Send ALA to an address")
        print("  balance <address>    - Check address balance")
        print("  status              - Show blockchain status")
        print("  validate            - Validate the entire chain")
        print("  help               - Show this help message")
        print("\n💡 Example:")
        print("  python main.py mine miner1")
        print("  python main.py send miner1 user1 100")
        print("  python main.py balance miner1")
        return
    
    command = sys.argv[1].lower()
    
    if command == "help":
        print_header()
        print("\n📚 Available Commands:")
        print("  mine [address]       - Mine a new block")
        print("  send <from> <to> <amount> - Send ALA to an address")
        print("  balance <address>    - Check address balance")
        print("  status              - Show blockchain status")
        print("  validate            - Validate the entire chain")
    
    elif command == "mine":
        if len(sys.argv) < 3:
            print("❌ Usage: python main.py mine [miner_address]")
            return
        miner_address = sys.argv[2]
        print(f"\n🔨 Mining block as {miner_address}...")
        start_time = time.time()
        block = blockchain.mine_pending_transactions(miner_address)
        if block:
            elapsed = time.time() - start_time
            print(f"\n✅ Successfully mined block in {elapsed:.2f} seconds!")
            print(f"   Block Hash: {block.hash}")
            print(f"   Block Index: {block.index}")
            print(f"   Transactions: {len(block.transactions)}")
            print(f"   Fee Reward: {block.fee_reward} ALA")
        else:
            print("❌ No transactions to mine or mining failed")
    
    elif command == "send":
        if len(sys.argv) < 5:
            print("❌ Usage: python main.py send <from> <to> <amount>")
            return
        sender = sys.argv[2]
        receiver = sys.argv[3]
        try:
            amount = int(sys.argv[4])
        except ValueError:
            print("❌ Amount must be a number")
            return
        
        print(f"\n💸 Sending {amount} ALA from {sender} to {receiver}...")
        tx_id = blockchain.add_transaction(sender, receiver, amount)
        if tx_id:
            print(f"✅ Transaction created: {tx_id}")
            print(f"   5% Fee: {int(amount * 0.05)} ALA")
            print(f"   Total Cost: {amount + int(amount * 0.05)} ALA")
        else:
            print("❌ Transaction failed (check sender balance)")
    
    elif command == "balance":
        if len(sys.argv) < 3:
            print("❌ Usage: python main.py balance [address]")
            return
        address = sys.argv[2]
        balance = blockchain.get_balance(address)
        print(f"\n💰 Balance for {address}: {balance} ALA")
    
    elif command == "status":
        print_header()
        print(f"\n📊 Blockchain Status:")
        print(f"   Blocks: {len(blockchain.chain)}")
        print(f"   Total Supply: {blockchain.total_supply} ALA")
        print(f"   Current Difficulty: {blockchain.difficulty}")
        print(f"   Current Mining Reward: {blockchain.mining_reward} ALA")
        print(f"   Pending Transactions: {len(blockchain.pending_transactions)}")
        print(f"   Last Block Hash: {blockchain.get_latest_block().hash}")
        print(f"   Chain Valid: {blockchain.is_chain_valid()}")
    
    elif command == "validate":
        print("\n🔍 Validating blockchain...")
        if blockchain.is_chain_valid():
            print("✅ Blockchain is valid!")
        else:
            print("❌ Blockchain validation failed!")
    
    else:
        print(f"❌ Unknown command: {command}")
        print("   Use 'help' for available commands")


if __name__ == "__main__":
    main()
