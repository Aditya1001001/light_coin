# Light Coin 🪙

A functional blockchain implementation built from scratch in Python, demonstrating core distributed systems concepts including transaction broadcasting, block validation, consensus mechanisms, and chain conflict resolution.

## 🎯 Project Overview

Light Coin is an educational blockchain project that implements the fundamental principles of cryptocurrency systems. Built entirely in Python with a Flask REST API, it provides a hands-on exploration of how blockchains work under the hood.

### Key Features

- **Proof of Work Consensus**: Mining algorithm with adjustable difficulty
- **Transaction Broadcasting**: Peer-to-peer transaction propagation across nodes
- **Wallet System**: Public/private key cryptography for secure transactions
- **Chain Conflict Resolution**: Longest chain rule for consensus across the network
- **REST API**: Full HTTP interface for node communication and blockchain interaction
- **Multi-Node Support**: Run multiple nodes simultaneously to simulate a distributed network

## 🏗️ Architecture

```
light_coin/
├── blockchain.py       # Core blockchain logic and chain management
├── block.py           # Block structure and validation
├── transaction.py     # Transaction creation and verification
├── wallet.py          # Wallet management and cryptographic signing
├── node.py           # Flask REST API for node communication
├── CLI_node.py       # Command-line interface for node operations
└── Utilities/        # Helper functions and utilities
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Aditya1001001/light_coin.git
cd light_coin
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running a Node

Start a blockchain node on port 5001:
```bash
python node.py -p 5001
```

Start additional nodes on different ports to simulate a network:
```bash
python node.py -p 5002
python node.py -p 5003
```

### Using the CLI

Interact with your node using the command-line interface:
```bash
python CLI_node.py
```

## 🔧 API Endpoints

### Blockchain Operations

- `GET /chain` - Retrieve the full blockchain
- `GET /mine` - Mine a new block
- `POST /transaction` - Create a new transaction
- `GET /transactions` - View pending transactions

### Network Operations

- `POST /node/register` - Register a new node in the network
- `GET /node/resolve` - Resolve chain conflicts using consensus algorithm
- `GET /nodes` - List all registered nodes

### Wallet Operations

- `POST /wallet/create` - Generate a new wallet
- `GET /wallet/balance` - Check wallet balance

## 📚 How It Works

### 1. Transaction Creation
When a user creates a transaction, it's signed with their private key and broadcast to all nodes in the network:

```python
# Example transaction structure
{
    "sender": "public_key_here",
    "recipient": "recipient_public_key",
    "amount": 10,
    "signature": "transaction_signature"
}
```

### 2. Mining Process
Nodes compete to mine new blocks by solving a proof-of-work puzzle:
- Collect pending transactions
- Find a nonce that produces a hash with required leading zeros
- Broadcast the new block to the network

### 3. Consensus Mechanism
When conflicts arise (multiple valid chains), nodes use the **longest chain rule**:
- Query all nodes for their chains
- Compare chain lengths and validity
- Adopt the longest valid chain

### 4. Chain Validation
Each block and the entire chain undergoes validation:
- Hash integrity checks
- Proof of work verification
- Transaction signature validation
- Previous hash linking

## 🔐 Cryptographic Components

- **Hashing**: SHA-256 for block hashing and proof of work
- **Digital Signatures**: RSA for transaction signing and verification
- **Public/Private Keys**: Secure wallet management

## 🎓 Educational Value

This project demonstrates understanding of:

- **Distributed Systems**: Peer-to-peer networking and consensus
- **Cryptography**: Hash functions, digital signatures, public-key infrastructure
- **Data Structures**: Linked list implementation via block hashing
- **API Design**: RESTful architecture for blockchain interaction
- **Conflict Resolution**: Byzantine fault tolerance principles

## 🧪 Testing

Run multiple nodes locally to simulate a distributed network:

```bash
# Terminal 1
python node.py -p 5001

# Terminal 2
python node.py -p 5002

# Terminal 3 - Register nodes with each other
curl -X POST http://localhost:5001/node/register -H "Content-Type: application/json" -d '{"nodes": ["http://localhost:5002"]}'
```

Create transactions, mine blocks on different nodes, and observe consensus in action.

## 🛠️ Technical Stack

- **Language**: Python 3
- **Web Framework**: Flask
- **Cryptography**: hashlib (SHA-256), Crypto (RSA)
- **Data Persistence**: File-based storage (JSON)


## 📖 Learning Resources

Built while learning from:
- Bitcoin whitepaper by Satoshi Nakamoto
- "Mastering Bitcoin" by Andreas Antonopoulos
- Various blockchain development tutorials and documentation

## 👤 Author

**Aditya Singh**
- GitHub: [@Aditya1001001](https://github.com/Aditya1001001)
- LinkedIn: [aditya1001001](https://linkedin.com/in/aditya1001001)

## 📄 License

This project is open source and available for educational purposes.

---

**Note**: This is an educational project and should not be used for production cryptocurrency applications. It's designed to demonstrate blockchain concepts and is not optimized for security or scalability at an enterprise level.
