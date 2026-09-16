"""
Alara Blockchain - P2P Network Implementation
Decentralized networking for the Alara blockchain.
"""

import json
import socket
import threading
import time
from typing import List, Dict, Any, Optional, Callable
from .blockchain import AlaraBlockchain
from .block import Block


class AlaraNode:
    """
    A P2P node for the Alara blockchain.
    Handles connections to other peers and blockchain synchronization.
    """
    
    def __init__(self, blockchain: AlaraBlockchain, host: str = "0.0.0.0", port: int = 5000):
        """
        Initialize the Alara node.
        
        Args:
            blockchain: The AlaraBlockchain instance
            host: Host address to bind to
            port: Port to listen on
        """
        self.blockchain = blockchain
        self.host = host
        self.port = port
        self.peers: List[Dict[str, Any]] = []  # List of connected peers
        self.running = False
        self.server_socket: Optional[socket.socket] = None
        self.peer_threads: List[threading.Thread] = []
        
        # Default peers (can be loaded from a config file)
        self.default_peers = [
            # Add your seed nodes here
            # {"host": "seed1.alara.net", "port": 5000},
            # {"host": "seed2.alara.net", "port": 5000},
        ]
    
    def start(self) -> None:
        """Start the P2P node."""
        self.running = True
        
        # Start the server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        
        print(f"🌐 Alara node started on {self.host}:{self.port}")
        
        # Start accepting connections in a separate thread
        accept_thread = threading.Thread(target=self._accept_connections, daemon=True)
        accept_thread.start()
        self.peer_threads.append(accept_thread)
        
        # Connect to default peers
        for peer in self.default_peers:
            self.connect_to_peer(peer["host"], peer["port"])
    
    def stop(self) -> None:
        """Stop the P2P node."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        for thread in self.peer_threads:
            thread.join()
        print("🛑 Alara node stopped")
    
    def _accept_connections(self) -> None:
        """Accept incoming peer connections."""
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f"🔌 New connection from {addr[0]}:{addr[1]}")
                
                # Start a new thread to handle this connection
                peer_thread = threading.Thread(
                    target=self._handle_peer,
                    args=(client_socket,),
                    daemon=True
                )
                peer_thread.start()
                self.peer_threads.append(peer_thread)
            except Exception as e:
                if self.running:
                    print(f"⚠️ Error accepting connection: {e}")
                break
    
    def connect_to_peer(self, host: str, port: int) -> bool:
        """
        Connect to a peer node.
        
        Args:
            host: Peer host address
            port: Peer port
            
        Returns:
            True if connection succeeded, False otherwise
        """
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            
            # Add to peers list
            self.peers.append({"host": host, "port": port, "socket": client_socket})
            
            # Start a thread to handle this connection
            peer_thread = threading.Thread(
                target=self._handle_peer,
                args=(client_socket,),
                daemon=True
            )
            peer_thread.start()
            self.peer_threads.append(peer_thread)
            
            print(f"✅ Connected to peer {host}:{port}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to {host}:{port}: {e}")
            return False
    
    def _handle_peer(self, client_socket: socket.socket) -> None:
        """Handle communication with a peer."""
        try:
            while self.running:
                # Receive data from peer
                data = client_socket.recv(4096).decode()
                if not data:
                    break
                
                # Parse the message
                try:
                    message = json.loads(data)
                    self._process_message(message, client_socket)
                except json.JSONDecodeError:
                    print(f"⚠️ Invalid JSON received: {data[:50]}")
                    continue
        except Exception as e:
            print(f"⚠️ Error with peer: {e}")
        finally:
            client_socket.close()
    
    def _process_message(self, message: Dict[str, Any], client_socket: socket.socket) -> None:
        """Process a message from a peer."""
        message_type = message.get("type")
        
        if message_type == "block":
            self._handle_block_message(message, client_socket)
        elif message_type == "transaction":
            self._handle_transaction_message(message, client_socket)
        elif message_type == "get_chain":
            self._handle_get_chain_message(client_socket)
        elif message_type == "chain":
            self._handle_chain_message(message, client_socket)
        elif message_type == "ping":
            self._send_message(client_socket, {"type": "pong"})
        elif message_type == "pong":
            pass  # Just acknowledge
        else:
            print(f"⚠️ Unknown message type: {message_type}")
    
    def _handle_block_message(self, message: Dict[str, Any], client_socket: socket.socket) -> None:
        """Handle a new block message from a peer."""
        block_data = message.get("data")
        if block_data:
            # Create a Block object from the data
            block = Block(
                index=block_data["index"],
                transactions=block_data["transactions"],
                previous_hash=block_data["previous_hash"],
                miner=block_data.get("miner", "0"),
                timestamp=block_data["timestamp"],
                nonce=block_data["nonce"]
            )
            
            # Check if we need to add this block
            latest_block = self.blockchain.get_latest_block()
            
            if block.index > latest_block.index:
                # This is a new block we don't have
                if block.previous_hash == latest_block.hash:
                    # This is the next block in the chain
                    print(f"📦 Received new block {block.index} from peer")
                    # In a real implementation, we would add it to our chain
                    # For now, just print it
                else:
                    # This might be from a fork, request the full chain
                    print(f"🔄 Possible fork detected, requesting full chain from peer")
                    self._send_message(client_socket, {"type": "get_chain"})
            else:
                # We already have this block or an older one
                pass
    
    def _handle_transaction_message(self, message: Dict[str, Any], client_socket: socket.socket) -> None:
        """Handle a new transaction message from a peer."""
        tx = message.get("data")
        if tx:
            print(f"📝 Received transaction from peer: {tx.get('tx_id', 'unknown')}")
            # In a real implementation, we would add it to our pending transactions
            # For now, just print it
    
    def _handle_get_chain_message(self, client_socket: socket.socket) -> None:
        """Handle a request for the full chain."""
        print("📤 Sending full chain to peer")
        chain_data = [block.to_dict() for block in self.blockchain.chain]
        self._send_message(client_socket, {
            "type": "chain",
            "data": chain_data,
            "length": len(chain_data)
        })
    
    def _handle_chain_message(self, message: Dict[str, Any], client_socket: socket.socket) -> None:
        """Handle a full chain message from a peer."""
        chain_data = message.get("data")
        if chain_data:
            print(f"📥 Received chain with {len(chain_data)} blocks from peer")
            # In a real implementation, we would validate and potentially replace our chain
            # For now, just print the length
    
    def _send_message(self, socket: socket.socket, message: Dict[str, Any]) -> None:
        """Send a message to a peer."""
        try:
            socket.sendall(json.dumps(message).encode())
        except Exception as e:
            print(f"⚠️ Failed to send message: {e}")
    
    def broadcast_block(self, block: Block) -> None:
        """Broadcast a new block to all connected peers."""
        message = {
            "type": "block",
            "data": block.to_dict()
        }
        for peer in self.peers:
            try:
                peer["socket"].sendall(json.dumps(message).encode())
            except Exception as e:
                print(f"⚠️ Failed to send block to {peer['host']}:{peer['port']}: {e}")
    
    def broadcast_transaction(self, transaction: Dict[str, Any]) -> None:
        """Broadcast a new transaction to all connected peers."""
        message = {
            "type": "transaction",
            "data": transaction
        }
        for peer in self.peers:
            try:
                peer["socket"].sendall(json.dumps(message).encode())
            except Exception as e:
                print(f"⚠️ Failed to send transaction to {peer['host']}:{peer['port']}: {e}")
    
    def add_peer(self, host: str, port: int) -> None:
        """Add a peer to the peers list."""
        if {"host": host, "port": port} not in self.peers:
            self.peers.append({"host": host, "port": port})
            print(f"✅ Added peer: {host}:{port}")
    
    def discover_peers(self) -> None:
        """
        Discover peers on the network.
        In a real implementation, this would use a seed node or DNS seeds.
        """
        # For now, just connect to default peers
        for peer in self.default_peers:
            self.connect_to_peer(peer["host"], peer["port"])
